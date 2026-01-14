import sqlite3

# SQLファイルの中身を読み込む
with open('reset_data.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

# データベースに接続（shop.db）
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

try:
    # SQLを順番に実行
    cursor.executescript(sql)
    conn.commit()
    print("データベースの更新に成功しました！")
except sqlite3.Error as e:
    print(f"エラーが発生しました: {e}")
finally:
    conn.close()