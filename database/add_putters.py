import sqlite3
import os

# ---------------------------------------------------------
# パス設定
# ---------------------------------------------------------
# このファイル(databaseフォルダ内)を基準にパスを設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, 'shop.db')
sql_path = os.path.join(BASE_DIR, 'add_putters.sql')

# ---------------------------------------------------------
# データ追加処理
# ---------------------------------------------------------
# SQLファイルの読み込み
with open(sql_path, 'r', encoding='utf-8') as f:
    sql = f.read()

# データベース接続
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # SQL実行
    cursor.executescript(sql)
    conn.commit()
    print("✅ パターのデータを追加しました！")
except sqlite3.Error as e:
    print(f"❌ エラーが発生しました: {e}")
finally:
    conn.close()