from flask import Flask

# Flaskアプリを作ります（これがWebサーバーの本体です）
app = Flask(__name__)

# トップページ（/）にアクセスが来た時の動き
@app.route('/')
def home():
    return """
    <h1>在庫管理システムへようこそ</h1>
    <p>Webサーバーが正常に起動しています。</p>
    <p>次はデータベースと接続します。</p>
    """

# このプログラムが直接実行されたらサーバーを起動する
if __name__ == '__main__':
    app.run(debug=True, port=5000)