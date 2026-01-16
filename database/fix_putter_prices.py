import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'shop.db')

# ---------------------------------------------------------
# パターの在庫・価格を強制登録するSQL
# ---------------------------------------------------------
# 一度パターの在庫データを削除してから、正しい価格で登録し直します
sql = """
-- 1. Odyssey Ai-ONE #1
DELETE FROM inventory WHERE product_id = (SELECT id FROM products WHERE name = 'Odyssey Ai-ONE #1');
INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name = 'Odyssey Ai-ONE #1'), '-', 41580, 550, 34.0, 8);

-- 2. Spider Tour X
DELETE FROM inventory WHERE product_id = (SELECT id FROM products WHERE name = 'Spider Tour X');
INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name = 'Spider Tour X'), '-', 48400, 560, 34.0, 5);

-- 3. Super Select Newport 2
DELETE FROM inventory WHERE product_id = (SELECT id FROM products WHERE name = 'Super Select Newport 2');
INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name = 'Super Select Newport 2'), '-', 66000, 540, 34.0, 3);
"""

# ---------------------------------------------------------
# 実行
# ---------------------------------------------------------
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.executescript(sql)
    conn.commit()
    print(f"✅ パター3種の価格データを修復しました！\n場所: {db_path}")
except sqlite3.Error as e:
    print(f"❌ エラーが発生しました: {e}")
finally:
    conn.close()