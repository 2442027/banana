import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = 'gstyle_golf_shop_key'

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MANAGER_PASSWORD = "master14"

def get_db_connection():
    db_path = os.path.join('database', 'shop.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# --- 認証系 ---
@app.route('/login', methods=['POST'])
def login():
    if request.form.get('password') == MANAGER_PASSWORD:
        session['is_manager'] = True
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('is_manager', None)
    return redirect(url_for('index'))

# --- メイン機能 ---
@app.route('/')
def index():
    is_manager = session.get('is_manager', False)
    conn = get_db_connection()
    # デフォルトは新しい順（ID降順）
    items = conn.execute("""
        SELECT p.*, m.name as maker_name, MIN(i.price) as min_price, MIN(i.stock) as min_stock
        FROM products p 
        JOIN makers m ON p.maker_id = m.id
        LEFT JOIN inventory i ON p.id = i.product_id 
        GROUP BY p.id
        ORDER BY p.id DESC
    """).fetchall()
    conn.close()
    
    # indexページでは検索条件は空っぽなので空の辞書を渡す
    return render_template('index.html', items=items, is_search=False, is_manager=is_manager, search_params={})

@app.route('/detail/<int:id>')
def detail(id):
    is_manager = session.get('is_manager', False)
    conn = get_db_connection()
    item = conn.execute("""
        SELECT p.*, m.name as maker_name 
        FROM products p 
        JOIN makers m ON p.maker_id = m.id 
        WHERE p.id = ?
    """, (id,)).fetchone()
    specs = conn.execute('SELECT * FROM inventory WHERE product_id = ?', (id,)).fetchall()
    conn.close()
    if item is None: return "商品が見つかりません", 404
    return render_template('detail.html', item=item, specs=specs, is_manager=is_manager)

@app.route('/search', methods=['GET', 'POST'])
def search():
    is_manager = session.get('is_manager', False)
    conn = get_db_connection()
    
    # 検索用の変数を初期化
    search_params = {}

    if request.method == 'POST':
        # フォーム値の取得
        m_id = request.form.get('maker_id')
        c_type = request.form.get('club_type')
        tag = request.form.get('tag')
        p_max = request.form.get('price_max')
        w_min = request.form.get('weight_min')
        w_max = request.form.get('weight_max')
        l_min = request.form.get('length_min')
        l_max = request.form.get('length_max')
        sort_order = request.form.get('sort_order') # ★並び順を取得

        # ★現在の検索条件を辞書に保存（これをHTMLに送り返す）
        search_params = {
            'maker_id': m_id, 'club_type': c_type, 'tag': tag,
            'price_max': p_max, 'weight_min': w_min, 'weight_max': w_max,
            'length_min': l_min, 'length_max': l_max, 'sort_order': sort_order
        }

        sql = """
            SELECT p.*, m.name as maker_name, MIN(i.price) as min_price, MIN(i.stock) as min_stock
            FROM products p JOIN makers m ON p.maker_id = m.id
            JOIN inventory i ON p.id = i.product_id WHERE 1=1
        """
        params = []
        if m_id: sql += " AND p.maker_id = ?"; params.append(m_id)
        if c_type: sql += " AND p.club_type = ?"; params.append(c_type)
        if tag: sql += " AND p.tag = ?"; params.append(tag)
        if p_max: sql += " AND i.price <= ?"; params.append(p_max)
        if w_min: sql += " AND i.weight >= ?"; params.append(w_min)
        if w_max: sql += " AND i.weight <= ?"; params.append(w_max)
        if l_min: sql += " AND i.length >= ?"; params.append(l_min)
        if l_max: sql += " AND i.length <= ?"; params.append(l_max)

        sql += " GROUP BY p.id"

        # ★並び替えロジック
        if sort_order == 'price_asc':
            sql += " ORDER BY min_price ASC"
        elif sort_order == 'price_desc':
            sql += " ORDER BY min_price DESC"
        else:
            sql += " ORDER BY p.id DESC" # デフォルトは新着順

        items = conn.execute(sql, params).fetchall()
        
        tags = conn.execute('SELECT DISTINCT tag FROM products WHERE tag IS NOT NULL').fetchall()
        conn.close()
        # ★ search_params を渡して、HTML側で「今の条件」を維持できるようにする
        return render_template('index.html', items=items, is_search=True, is_manager=is_manager, search_params=search_params)

    # GETアクセスの場合は検索画面表示
    makers = conn.execute('SELECT * FROM makers').fetchall()
    club_types = conn.execute('SELECT DISTINCT club_type FROM products').fetchall()
    tags = conn.execute('SELECT DISTINCT tag FROM products WHERE tag IS NOT NULL').fetchall()
    conn.close()
    return render_template('search.html', makers=makers, club_types=club_types, tags=tags)

# --- 管理者機能（add, edit, delete は変更なしのため省略しますが、既存のコードのまま使えます） ---
@app.route('/add', methods=['GET', 'POST'])
def add():
    if not session.get('is_manager'): return redirect(url_for('index'))
    conn = get_db_connection()
    if request.method == 'POST':
        maker_name = request.form['maker_name']
        maker = conn.execute('SELECT id FROM makers WHERE name = ?', (maker_name,)).fetchone()
        if maker: maker_id = maker['id']
        else:
            cursor = conn.execute('INSERT INTO makers (name) VALUES (?)', (maker_name,))
            maker_id = cursor.lastrowid
        image_file_name = None
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_file_name = filename
        conn.execute('INSERT INTO products (maker_id, name, club_type, tag, description, image_file) VALUES (?, ?, ?, ?, ?, ?)',
                     (maker_id, request.form['name'], request.form['club_type'], request.form['tag'], request.form['description'], image_file_name))
        conn.commit(); conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not session.get('is_manager'): return redirect(url_for('index'))
    conn = get_db_connection()
    if request.method == 'POST':
        conn.execute("UPDATE products SET maker_id=?, name=?, club_type=?, tag=?, description=?, image_file=? WHERE id=?",
                     (request.form['maker_id'], request.form['name'], request.form['club_type'], request.form['tag'], request.form['description'], request.form['image_file'], id))
        spec_ids = request.form.getlist('spec_id')
        for sid in spec_ids:
            conn.execute("UPDATE inventory SET flex=?, weight=?, length=?, price=?, stock=? WHERE id=?",
                         (request.form.get(f'flex_{sid}'), request.form.get(f'weight_{sid}'), request.form.get(f'length_{sid}'), request.form.get(f'price_{sid}'), request.form.get(f'stock_{sid}'), sid))
        conn.commit(); conn.close()
        return redirect(url_for('detail', id=id))
    item = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    specs = conn.execute('SELECT * FROM inventory WHERE product_id = ?', (id,)).fetchall()
    makers = conn.execute('SELECT * FROM makers').fetchall()
    conn.close()
    return render_template('edit.html', item=item, makers=makers, specs=specs)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if not session.get('is_manager'): return redirect(url_for('index'))
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.execute('DELETE FROM inventory WHERE product_id = ?', (id,))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)