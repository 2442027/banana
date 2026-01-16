import sqlite3
import os

# データベースパスの設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'shop.db')

# ---------------------------------------------------------
# 価格更新用SQL (実勢価格ベース)
# ---------------------------------------------------------
sql = """
-- 1. ドライバー (DR)
UPDATE inventory SET price = 96800 WHERE product_id = (SELECT id FROM products WHERE name = 'Qi10 MAX');
UPDATE inventory SET price = 86900 WHERE product_id = (SELECT id FROM products WHERE name = 'PARADYM Ai SMOKE');
UPDATE inventory SET price = 93500 WHERE product_id = (SELECT id FROM products WHERE name = 'G430 MAX');

-- 2. パター (PT)
UPDATE inventory SET price = 41580 WHERE product_id = (SELECT id FROM products WHERE name = 'Odyssey Ai-ONE #1');
UPDATE inventory SET price = 48400 WHERE product_id = (SELECT id FROM products WHERE name = 'Spider Tour X');
UPDATE inventory SET price = 66000 WHERE product_id = (SELECT id FROM products WHERE name = 'Super Select Newport 2');

-- 3. フェアウェイウッド (FW)
UPDATE inventory SET price = 60500 WHERE product_id = (SELECT id FROM products WHERE name = 'G430 MAX FW');
UPDATE inventory SET price = 68200 WHERE product_id = (SELECT id FROM products WHERE name = 'Qi10 Tour FW');
UPDATE inventory SET price = 59400 WHERE product_id = (SELECT id FROM products WHERE name = 'PARADYM Ai SMOKE MAX FW');

-- 4. アイアンセット (Iron - 5本セットまたは6本セット想定)
UPDATE inventory SET price = 184800 WHERE product_id = (SELECT id FROM products WHERE name = 'P790 アイアン');
UPDATE inventory SET price = 184800 WHERE product_id = (SELECT id FROM products WHERE name = 'T100 アイアン');
UPDATE inventory SET price = 145200 WHERE product_id = (SELECT id FROM products WHERE name = 'G430 アイアン');

-- 5. ウェッジ (Wedge)
UPDATE inventory SET price = 27500 WHERE product_id = (SELECT id FROM products WHERE name = 'Vokey SM10');
UPDATE inventory SET price = 26400 WHERE product_id = (SELECT id FROM products WHERE name = 'JAWS Raw');
UPDATE inventory SET price = 27500 WHERE product_id = (SELECT id FROM products WHERE name = 'Milled Grind 4');
"""

# ---------------------------------------------------------
# 実行処理
# ---------------------------------------------------------
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.executescript(sql)
    conn.commit()
    print(f"✅ 全商品の価格を最新の市場価格に更新しました！\nDB場所: {db_path}")
except sqlite3.Error as e:
    print(f"❌ エラーが発生しました: {e}")
finally:
    conn.close()