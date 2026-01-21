import os
from flask import Flask, render_template, request, redirect, url_for, session, flash # ★flashを追加
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = 'gstyle_golf_shop_key'

# 画像保存先の設定
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 管理者パスワード
MANAGER_PASSWORD = "master14"

# ---------------------------------------------------------
# データベース接続
# ---------------------------------------------------------
def get_db_connection():
    db_path = os.path.join('database', 'shop.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------------------------------------
# 認証機能
# ---------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    if request.form.get('password') == MANAGER_PASSWORD:
        session['is_manager'] = True
        flash('管理者としてログインしました', 'success') # ログイン成功メッセージ
    else:
        flash('パスワードが違います', 'danger')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('is_manager', None)
    flash('ログアウトしました', 'info')
    return redirect(url_for('index'))

# ---------------------------------------------------------
# 1. 商品一覧
# ---------------------------------------------------------
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
        ORDER BY p.id DESC
    """).fetchall()
    conn.close()
    return render_template('index.html', items=items, is_search=False, is_manager=is_manager, search_params={})

# ---------------------------------------------------------
# 2. 商品詳細 (リロード対策済み)
# ---------------------------------------------------------
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
    
    # ★ここがポイント：商品が無ければホームに戻す
    if item is None:
        conn.close()
        flash('⚠️ お探しの商品は削除されたか、存在しません。', 'warning')
        return redirect(url_for('index'))
    
    specs = conn.execute('SELECT * FROM inventory WHERE product_id = ? ORDER BY price', (id,)).fetchall()
    conn.close()
    
    return render_template('detail.html', item=item, specs=specs, is_manager=is_manager)

# ---------------------------------------------------------
# 3. 検索機能
# ---------------------------------------------------------
@app.route('/search', methods=['GET', 'POST'])
def search():
    is_manager = session.get('is_manager', False)
    conn = get_db_connection()
    search_params = {}

    if request.method == 'POST':
        # (検索ロジックは変更なし)
        m_id = request.form.get('maker_id')
        c_type = request.form.get('club_type')
        tag = request.form.get('tag')
        p_max = request.form.get('price_max')
        w_min = request.form.get('weight_min')
        w_max = request.form.get('weight_max')
        l_min = request.form.get('length_min')
        l_max = request.form.get('length_max')
        sort_order = request.form.get('sort_order')

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
        if sort_order == 'price_asc': sql += " ORDER BY min_price ASC"
        elif sort_order == 'price_desc': sql += " ORDER BY min_price DESC"
        else: sql += " ORDER BY p.id DESC"

        items = conn.execute(sql, params).fetchall()
        tags = conn.execute('SELECT DISTINCT tag FROM products WHERE tag IS NOT NULL').fetchall()
        conn.close()
        return render_template('index.html', items=items, is_search=True, is_manager=is_manager, search_params=search_params)

    makers = conn.execute('SELECT * FROM makers').fetchall()
    club_types = conn.execute('SELECT DISTINCT club_type FROM products').fetchall()
    tags = conn.execute('SELECT DISTINCT tag FROM products WHERE tag IS NOT NULL').fetchall()
    conn.close()
    return render_template('search.html', makers=makers, club_types=club_types, tags=tags)

# ---------------------------------------------------------
# 4. 比較機能
# ---------------------------------------------------------
@app.route('/compare')
def compare():
    ids = request.args.getlist('product_ids')
    if not ids: return redirect(url_for('index'))
    
    conn = get_db_connection()
    # プレースホルダー作成
    placeholders = ',' .join(['?'] * len(ids))
    sql = f"SELECT p.*, m.name as maker_name FROM products p JOIN makers m ON p.maker_id = m.id WHERE p.id IN ({placeholders})"
    products = conn.execute(sql, ids).fetchall()
    
    # ★ここでもチェック：もし選んだ商品が全部消されてたらホームへ
    if not products:
        conn.close()
        flash('⚠️ 選択した商品は削除されています。', 'warning')
        return redirect(url_for('index'))

    specs_map = {}
    for p in products:
        specs = conn.execute('SELECT * FROM inventory WHERE product_id = ? ORDER BY price', (p['id'],)).fetchall()
        specs_map[p['id']] = specs

    conn.close()
    return render_template('compare.html', products=products, specs_map=specs_map)

# ---------------------------------------------------------
# 5. 管理者機能 (追加・編集・削除)
# ---------------------------------------------------------
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
        flash('商品を新規登録しました', 'success')
        return redirect(url_for('index'))
    conn.close()
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not session.get('is_manager'): return redirect(url_for('index'))
    conn = get_db_connection()
    
    # 存在チェック
    item = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    if item is None:
        conn.close()
        flash('⚠️ 編集しようとした商品は既に削除されています。', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        conn.execute("UPDATE products SET maker_id=?, name=?, club_type=?, tag=?, description=?, image_file=? WHERE id=?",
                     (request.form['maker_id'], request.form['name'], request.form['club_type'], request.form['tag'], request.form['description'], request.form['image_file'], id))
        
        spec_ids = request.form.getlist('spec_id')
        for sid in spec_ids:
            conn.execute("UPDATE inventory SET flex=?, weight=?, length=?, price=?, stock=? WHERE id=?",
                         (request.form.get(f'flex_{sid}'), request.form.get(f'weight_{sid}'), request.form.get(f'length_{sid}'), request.form.get(f'price_{sid}'), request.form.get(f'stock_{sid}'), sid))
        conn.commit(); conn.close()
        flash('商品情報を更新しました', 'success')
        return redirect(url_for('detail', id=id))
    
    specs = conn.execute('SELECT * FROM inventory WHERE product_id = ?', (id,)).fetchall()
    makers = conn.execute('SELECT * FROM makers').fetchall()
    conn.close()
    return render_template('edit.html', item=item, makers=makers, specs=specs)

@app.route('/add_spec/<int:product_id>', methods=['POST'])
def add_spec(product_id):
    if not session.get('is_manager'): return redirect(url_for('index'))
    conn = get_db_connection()
    
    # 親商品が存在するか確認
    check = conn.execute('SELECT id FROM products WHERE id = ?', (product_id,)).fetchone()
    if check is None:
        conn.close()
        flash('⚠️ エラー：対象の商品が存在しません。', 'danger')
        return redirect(url_for('index'))

    # フォームから値を取得
    flex = request.form.get('flex')
    weight = request.form.get('weight')
    length = request.form.get('length')
    price = request.form.get('price')
    stock = request.form.get('stock')
    
    if not price: price = 0
    if not weight: weight = 0
    if not stock: stock = 0
    
    conn.execute('INSERT INTO inventory (product_id, flex, weight, length, price, stock) VALUES (?, ?, ?, ?, ?, ?)',
                 (product_id, flex, weight, length, price, stock))
    conn.commit()
    conn.close()
    flash('新しいスペックを追加しました', 'success')
    return redirect(url_for('edit', id=product_id))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if not session.get('is_manager'): return redirect(url_for('index'))
    
    conn = get_db_connection()
    try:
        product = conn.execute('SELECT maker_id FROM products WHERE id = ?', (id,)).fetchone()
        
        if product:
            maker_id = product['maker_id']
            # 売上、在庫、商品を削除
            conn.execute('DELETE FROM sales WHERE inventory_id IN (SELECT id FROM inventory WHERE product_id = ?)', (id,))
            conn.execute('DELETE FROM inventory WHERE product_id = ?', (id,))
            conn.execute('DELETE FROM products WHERE id = ?', (id,))
            
            # メーカーお掃除
            count = conn.execute('SELECT COUNT(*) FROM products WHERE maker_id = ?', (maker_id,)).fetchone()[0]
            if count == 0:
                conn.execute('DELETE FROM makers WHERE id = ?', (maker_id,))
        
        conn.commit()
        flash('商品を削除しました', 'warning') # 削除は黄色（warning）で通知
    except Exception as e:
        conn.rollback()
        flash(f'削除中にエラーが発生しました: {e}', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('index'))

# ---------------------------------------------------------
# 6. 売上登録機能 (エラー対策済み)
# ---------------------------------------------------------
@app.route('/sell/<int:inv_id>', methods=['POST'])
def sell(inv_id):
    if not session.get('is_manager'): return redirect(url_for('index'))
    
    conn = get_db_connection()
    
    # 在庫情報を取得しようとする
    inv = conn.execute('SELECT stock, price, product_id FROM inventory WHERE id = ?', (inv_id,)).fetchone()
    
    # ★重要：もし削除されていたらここでブロック！
    if inv is None:
        conn.close()
        flash('⚠️ エラー：操作しようとした商品は、別の端末で削除されました。', 'danger')
        return redirect(url_for('index'))

    if inv['stock'] > 0:
        conn.execute('UPDATE inventory SET stock = stock - 1 WHERE id = ?', (inv_id,))
        conn.execute('INSERT INTO sales (inventory_id, price_at_sale) VALUES (?, ?)', (inv_id, inv['price']))
        conn.commit()
        flash('売上を登録しました！在庫が1つ減りました。', 'success')
    else:
        flash('在庫切れのため登録できませんでした。', 'warning')

    conn.close()
    return redirect(url_for('detail', id=inv['product_id']))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0')