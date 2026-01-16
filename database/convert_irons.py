import sqlite3
import os

# データベースパス
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'shop.db')

# ---------------------------------------------------------
# アイアンを単品(#7)に変更するSQL
# ---------------------------------------------------------
# セット価格を1本あたりの価格に修正し、商品名に「#7」をつける
sql = """
-- 1. P790 アイアン (Taylormade)
-- セット184,800円 → 単品 30,800円
UPDATE products SET name = 'P790 アイアン #7' WHERE name = 'P790 アイアン';
UPDATE inventory SET price = 30800, stock = 15 WHERE product_id = (SELECT id FROM products WHERE name = 'P790 アイアン #7');

-- 2. T100 アイアン (Titleist)
-- セット184,800円 → 単品 30,800円
UPDATE products SET name = 'T100 アイアン #7' WHERE name = 'T100 アイアン';
UPDATE inventory SET price = 30800, stock = 8 WHERE product_id = (SELECT id FROM products WHERE name = 'T100 アイアン #7');

-- 3. G430 アイアン (PING)
-- セット145,200円 → 単品 24,200円
UPDATE products SET name = 'G430 アイアン #7' WHERE name = 'G430 アイアン';
UPDATE inventory SET price = 24200, stock = 20 WHERE product_id = (SELECT id FROM products WHERE name = 'G430 アイアン #7');
"""

# ---------------------------------------------------------
# 実行
# ---------------------------------------------------------
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.executescript(sql)
    conn.commit()
    print(f"✅ アイアンを「セット」から「単品(#7)」データに変更しました！\n場所: {db_path}")
except sqlite3.Error as e:
    print(f"❌ エラーが発生しました: {e}")
finally:
    conn.close()