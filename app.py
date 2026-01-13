from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# データ保存用リスト（仮）
items = []

# --- 1. 一覧ページの表示 ---
@app.route('/')
def index():
    return render_template('index.html', items=items)

# --- 2. 登録ページの表示(GET) と 登録処理(POST) ---
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # フォームからデータを受け取る
        new_item = {
            'maker': request.form['maker'],
            'name': request.form['name'],
            'club_type': request.form['club_type'],
            'price': request.form['price'],
            'stock': request.form['stock']
        }
        items.append(new_item)
        # 登録が終わったら一覧ページに飛ばす
        return redirect('/')
    
    # GETリクエスト（ただページを開いた時）は登録画面を表示
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)