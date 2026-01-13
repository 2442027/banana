from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'shop.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON') # 外部キー制約を有効化
    return conn

# --- トップページ（一覧表示） ---
@app.route('/')
def index():
    query = '''
        SELECT 
            i.id, m.name AS maker, p.name AS name, p.club_type, 
            i.flex, i.price, i.weight, i.length, i.stock
        FROM inventory i
        JOIN products p ON i.product_id = p.id
        JOIN makers m ON p.maker_id = m.id
    '''
    with get_db() as conn:
        items = conn.execute(query).fetchall()
    return render_template('index.html', items=items)

# --- 商品登録 ---
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    conn = get_db()
    if request.method == 'POST':
        maker_id = request.form.get('maker_id')
        name = request.form.get('name')
        club_type = request.form.get('club_type')
        flex = request.form.get('flex')
        price = request.form.get('price')
        weight = request.form.get('weight')
        length = request.form.get('length')
        stock = request.form.get('stock')

        # 1. productsテーブルにモデルがあるか確認、なければ作成
        cur = conn.cursor()
        product = cur.execute('SELECT id FROM products WHERE name = ? AND maker_id = ?', (name, maker_id)).fetchone()
        if product:
            product_id = product['id']
        else:
            cur.execute('INSERT INTO products (maker_id, name, club_type) VALUES (?, ?, ?)', (maker_id, name, club_type))
            product_id = cur.lastrowid
        
        # 2. inventoryテーブルに在庫スペックを登録
        cur.execute('''
            INSERT INTO inventory (product_id, flex, price, weight, length, stock)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (product_id, flex, price, weight, length, stock))
        conn.commit()
        return redirect('/')

    # GET時：選択肢としてメーカー一覧を渡す
    makers = conn.execute('SELECT * FROM makers').fetchall()
    return render_template('add.html', makers=makers)

# --- 編集 ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    conn = get_db()
    if request.method == 'POST':
        # 在庫スペックのみ更新する簡易版
        flex = request.form.get('flex')
        price = request.form.get('price')
        weight = request.form.get('weight')
        length = request.form.get('length')
        stock = request.form.get('stock')
        
        conn.execute('''
            UPDATE inventory 
            SET flex=?, price=?, weight=?, length=?, stock=?
            WHERE id=?
        ''', (flex, price, weight, length, stock, id))
        conn.commit()
        return redirect('/')

    # 現在のデータを取得
    item = conn.execute('''
        SELECT i.*, p.name, m.name as maker_name 
        FROM inventory i 
        JOIN products p ON i.product_id = p.id 
        JOIN makers m ON p.maker_id = m.id 
        WHERE i.id = ?
    ''', (id,)).fetchone()
    return render_template('edit.html', item=item)

# --- 削除 ---
@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    with get_db() as conn:
        conn.execute('DELETE FROM inventory WHERE id = ?', (id,))
    return redirect('/')

# --- 検索 ---
@app.route('/search', methods=['GET', 'POST'])
def search_item():
    conn = get_db()
    makers = conn.execute('SELECT * FROM makers').fetchall()
    
    if request.method == 'POST':
        cond_maker = request.form.get('maker_id')
        cond_price_max = request.form.get('price_max')

        sql = '''
            SELECT i.*, m.name AS maker, p.name AS name, p.club_type
            FROM inventory i
            JOIN products p ON i.product_id = p.id
            JOIN makers m ON p.maker_id = m.id
            WHERE 1=1
        '''
        params = []
        if cond_maker:
            sql += " AND m.id = ?"
            params.append(cond_maker)
        if cond_price_max:
            sql += " AND i.price <= ?"
            params.append(cond_price_max)
        
        results = conn.execute(sql, params).fetchall()
        return render_template('search_results.html', items=results)

    return render_template('search.html', makers=makers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)