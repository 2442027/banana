import sqlite3
import os

# ---------------------------------------------------------
# ファイルパスの自動設定
# ---------------------------------------------------------
# __file__ はこのスクリプト自体のパス。
# os.path.dirname で「このファイルが入っているフォルダ(database)」の場所を取得します。
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# データベースファイルとSQLファイルの絶対パスを作成
# これにより、どのフォルダから実行しても正しくファイルを読み込めます
db_path = os.path.join(BASE_DIR, 'shop.db')
sql_path = os.path.join(BASE_DIR, 'reset_data.sql')

# ---------------------------------------------------------
# データベースの初期化処理
# ---------------------------------------------------------
# SQLファイルの中身をテキストとして読み込む
with open(sql_path, 'r', encoding='utf-8') as f:
    sql = f.read()

# データベースに接続
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # SQLを一括実行（テーブル削除 → 作成 → データ投入）
    cursor.executescript(sql)
    conn.commit()
    print(f"✅ データベースの初期化に成功しました！\n場所: {db_path}")
except sqlite3.Error as e:
    print(f"❌ エラーが発生しました: {e}")
finally:
    conn.close()