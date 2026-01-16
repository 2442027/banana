import sqlite3
import os

# データベースファイルのパス設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'shop.db')

# ---------------------------------------------------------
# 追加するデータのSQL
# ---------------------------------------------------------
sql = """
-- 1. フェアウェイウッド (FW)
INSERT INTO products (maker_id, name, club_type, tag, description, image_file) VALUES 
((SELECT id FROM makers WHERE name='PING'), 'G430 MAX FW', 'フェアウェイウッド', '初心者おすすめ', '「激飛」でおなじみ。とにかく曲がらず、球が上がりやすい安心感抜群のモデル。', 'image07.jpg'),
((SELECT id FROM makers WHERE name='Taylormade'), 'Qi10 Tour FW', 'フェアウェイウッド', 'アスリート向け', 'ロフト調整機能付きで、操作性が高い。パワーヒッターが叩けるモデル。', 'image08.jpg'),
((SELECT id FROM makers WHERE name='Callaway'), 'PARADYM Ai SMOKE MAX FW', 'フェアウェイウッド', '全レベル対応', 'どこで打っても飛ぶAIフェース。ミスヒットに強く、多くのゴルファーに合う。', 'image09.jpg');

-- FW在庫
INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name='G430 MAX FW'), 'SR', 60500, 315, 43.0, 12),
((SELECT id FROM products WHERE name='Qi10 Tour FW'), 'S', 65000, 325, 42.0, 4), -- 残りわずか
((SELECT id FROM products WHERE name='PARADYM Ai SMOKE MAX FW'), 'R', 58000, 310, 43.25, 0); -- 在庫切れ


-- 2. アイアンセット (Iron)
INSERT INTO products (maker_id, name, club_type, tag, description, image_file) VALUES 
((SELECT id FROM makers WHERE name='Taylormade'), 'P790 アイアン', 'アイアン', '中級者向け', '中空構造でカッコいいのにやさしくて飛ぶ。世界中で大ヒットしているモデル。', 'image10.jpg'),
((SELECT id FROM makers WHERE name='Titleist'), 'T100 アイアン', 'アイアン', 'アスリート向け', 'ツアープロ使用率No.1。正確な距離感と操作性を極めた軟鉄鍛造。', 'image11.jpg'),
((SELECT id FROM makers WHERE name='PING'), 'G430 アイアン', 'アイアン', '初心者おすすめ', 'ダフっても滑ってくれるワイドソール。高弾道でグリーンに止まるキャビティアイアン。', 'image12.jpg');

-- アイアン在庫
INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name='P790 アイアン'), 'S', 160000, 410, 37.0, 6),
((SELECT id FROM products WHERE name='T100 アイアン'), 'S200', 184800, 430, 37.0, 2), -- 残りわずか
((SELECT id FROM products WHERE name='G430 アイアン'), 'R', 140000, 370, 37.5, 10);


-- 3. ウェッジ (Wedge)
INSERT INTO products (maker_id, name, club_type, tag, description, image_file) VALUES 
((SELECT id FROM makers WHERE name='Titleist'), 'Vokey SM10', 'ウェッジ', '全レベル対応', 'ウェッジの金字塔。多彩なグラインドでどんなライにも対応。', 'image13.jpg'),
((SELECT id FROM makers WHERE name='Callaway'), 'JAWS Raw', 'ウェッジ', '中級者向け', 'フェースのメッキを排除してスピン性能を最大化。強烈に止まる。', 'image14.jpg'),
((SELECT id FROM makers WHERE name='Taylormade'), 'Milled Grind 4', 'ウェッジ', 'アスリート向け', '水に濡れてもスピンが落ちないレーザー加工。打感が柔らかい。', 'image15.jpg');

-- ウェッジ在庫
INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name='Vokey SM10'), 'S200', 27500, 460, 35.0, 20),
((SELECT id FROM products WHERE name='JAWS Raw'), 'S', 25000, 450, 35.25, 8),
((SELECT id FROM products WHERE name='Milled Grind 4'), 'S', 26400, 455, 35.0, 5); -- 残りわずか
"""

# ---------------------------------------------------------
# 実行処理
# ---------------------------------------------------------
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.executescript(sql)
    conn.commit()
    print(f"✅ 新しいクラブデータを9件追加しました！\n場所: {db_path}")
except sqlite3.Error as e:
    print(f"❌ エラーが発生しました: {e}")
finally:
    conn.close()