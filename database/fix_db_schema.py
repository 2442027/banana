import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'shop.db')

conn = sqlite3.connect(db_path)

# 1. salesテーブルがなければ作る
conn.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inventory_id INTEGER,
    price_at_sale INTEGER,
    sold_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (inventory_id) REFERENCES inventory(id)
);
""")

print("✅ データベース構造を修復しました（salesテーブルの確認完了）")
conn.commit()
conn.close()