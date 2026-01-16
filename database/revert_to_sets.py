import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'shop.db')

# ---------------------------------------------------------
# バラ売りを「5本セット」に戻すSQL
# ---------------------------------------------------------
sql = """
-- 1. まず、追加したバラ売り（#5, #9）のデータを完全に削除
DELETE FROM inventory WHERE product_id IN (SELECT id FROM products WHERE name LIKE '%#5%' OR name LIKE '%#9%');
DELETE FROM products WHERE name LIKE '%#5%' OR name LIKE '%#9%';

-- 2. 残っている「#7」のデータを「5本セット」に書き換え＆価格変更
--    価格は単純計算で「単品価格 × 5本」に設定します。

-- P790 (単品30,800円 × 5 = 154,000円)
UPDATE products SET 
    name = 'P790 アイアン 5本セット', 
    description = '【5本セット(#6-PW)】中空構造でカッコいいのにやさしくて飛ぶ。世界中で大ヒットしているモデル。'
WHERE name LIKE 'P790%#7%';

UPDATE inventory SET 
    price = 154000, 
    stock = 3 
WHERE product_id = (SELECT id FROM products WHERE name = 'P790 アイアン 5本セット');


-- T100 (単品30,800円 × 5 = 154,000円)
UPDATE products SET 
    name = 'T100 アイアン 5本セット', 
    description = '【5本セット(#6-PW)】ツアープロ使用率No.1。正確な距離感と操作性を極めた軟鉄鍛造。'
WHERE name LIKE 'T100%#7%';

UPDATE inventory SET 
    price = 154000, 
    stock = 2 
WHERE product_id = (SELECT id FROM products WHERE name = 'T100 アイアン 5本セット');


-- G430 (単品24,200円 × 5 = 121,000円)
UPDATE products SET 
    name = 'G430 アイアン 5本セット', 
    description = '【5本セット(#6-PW)】ダフっても滑ってくれるワイドソール。高弾道でグリーンに止まるキャビティアイアン。'
WHERE name LIKE 'G430%#7%';

UPDATE inventory SET 
    price = 121000, 
    stock = 5 
WHERE product_id = (SELECT id FROM products WHERE name = 'G430 アイアン 5本セット');
"""

# ---------------------------------------------------------
# 実行
# ---------------------------------------------------------
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.executescript(sql)
    conn.commit()
    print(f"✅ アイアンを「5本セット」に変更しました！\n場所: {db_path}")
except sqlite3.Error as e:
    print(f"❌ エラーが発生しました: {e}")
finally:
    conn.close()