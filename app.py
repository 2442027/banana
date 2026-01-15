import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = 'gstyle_golf_shop_key'

# 画像の保存先フォルダ
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 店長用パスワード
MANAGER_PASSWORD = "master14"

def get_db_connection():
    conn = sqlite3.connect('shop.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------------------
# 店長認証
# ---------------------------------------
@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == MANAGER_PASSWORD:
        session['is_manager'] = True
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('is_manager', None)
    return redirect(url_for('index'))

# ---------------------------------------
# 一覧・詳細・検索
# ---------------------------------------
@app.route('/')
def index():
    is_manager = session.get('is_manager', False)
    conn = get_db_connection()
    items = conn.execute("""
        SELECT p.*, m.name as maker_name, MIN(i.price) as min_price, MIN(i.stock) as min_stock
        FROM products p 
        JOIN makers m ON p.maker_id = m.id
        LEFT JOIN inventory i ON p.id = i.product_id 
        GROUP BY p.id
    """).fetchall()
    conn.close()
    return render_template('index.html', items=items, is_search=False, is_manager=is_manager)

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
    if request.method == 'POST':
        m_id = request.form.get('maker_id'); c_type = request.form.get('club_type')
        p_max = request.form.get('price_max'); w_min = request.form.get('weight_min')
        w_max = request.form.get('weight_max'); l_min = request.form.get('length_min')
        l_max = request.form.get('length_max')

        sql = """
            SELECT p.*, m.name as maker_name, MIN(i.price) as min_price, MIN(i.stock) as min_stock
            FROM products p JOIN makers m ON p.maker_id = m.id
            JOIN inventory i ON p.id = i.product_id WHERE 1=1
        """
        params = []
        if m_id: sql += " AND p.maker_id = ?"; params.append(m_id)
        if c_type: sql += " AND p.club_type = ?"; params.append(c_type)
        if p_max: sql += " AND i.price <= ?"; params.append(p_max)
        if w_min: sql += " AND i.weight >= ?"; params.append(w_min)
        if w_max: sql += " AND i.weight <= ?"; params.append(w_max)
        if l_min: sql += " AND i.length >= ?"; params.append(l_min)
        if l_max: sql += " AND i.length <= ?"; params.append(l_max)

        sql += " GROUP BY p.id"
        items = conn.execute(sql, params).fetchall()
        conn.close()
        return render_template('index.html', items=items, is_search=True, is_manager=is_manager)

    makers = conn.execute('SELECT * FROM makers').fetchall()
    club_types = conn.execute('SELECT DISTINCT club_type FROM products').fetchall()
    conn.close()
    return render_template('search.html', makers=makers, club_types=club_types)

# ---------------------------------------
# 管理機能（店長のみ）
# ---------------------------------------
@app.route('/add', methods=['GET', 'POST'])
def add():
    if not session.get('is_manager'): return redirect(url_for('index'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        # 1. メーカー処理（入力された名前が既存かチェック、なければ新規作成）
        maker_name = request.form['maker_name']
        maker = conn.execute('SELECT id FROM makers WHERE name = ?', (maker_name,)).fetchone()
        
        if maker:
            maker_id = maker['id']
        else:
            # 新しいメーカーなら登録してIDを取得
            cursor = conn.execute('INSERT INTO makers (name) VALUES (?)', (maker_name,))
            maker_id = cursor.lastrowid

        # 2. 画像アップロード処理
        image_file_name = None
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                # static/images フォルダに保存
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_file_name = filename

        # 3. 商品登録
        conn.execute('INSERT INTO products (maker_id, name, club_type, description, image_file) VALUES (?, ?, ?, ?, ?)',
                     (maker_id, request.form['name'], request.form['club_type'], request.form['description'], image_file_name))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('add.html') # メーカー一覧は不要になったので渡さない

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not session.get('is_manager'): return redirect(url_for('index'))
    conn = get_db_connection()
    if request.method == 'POST':
        # 基本情報の更新
        conn.execute("UPDATE products SET maker_id=?, name=?, club_type=?, description=?, image_file=? WHERE id=?",
                     (request.form['maker_id'], request.form['name'], request.form['club_type'], request.form['description'], request.form['image_file'], id))
        
        # スペック更新
        spec_ids = request.form.getlist('spec_id')
        for sid in spec_ids:
            conn.execute("UPDATE inventory SET flex=?, weight=?, length=?, price=?, stock=? WHERE id=?",
                         (request.form.get(f'flex_{sid}'), request.form.get(f'weight_{sid}'), request.form.get(f'length_{sid}'), 
                          request.form.get(f'price_{sid}'), request.form.get(f'stock_{sid}'), sid))
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
    # 保存先フォルダがない場合は作成
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)