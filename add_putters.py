import sqlite3

# SQLファイルを読み込む
with open('add_putters.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

# データベースに接続
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

try:
    # SQLを実行
    cursor.executescript(sql)
    conn.commit()
    print("✅ パターのデータを追加しました！")
except sqlite3.Error as e:
    print(f"❌ エラーが発生しました: {e}")
finally:
    conn.close()