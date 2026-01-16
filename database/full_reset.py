import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'shop.db')

# ---------------------------------------------------------
# 全データを再構築するSQL (これまでの集大成)
# ---------------------------------------------------------
sql = """
-- 1. テーブルを削除して真っさらにする
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS makers;

-- 2. テーブル作成 (タグ機能付き)
CREATE TABLE makers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    country TEXT
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maker_id INTEGER,
    name TEXT NOT NULL,
    club_type TEXT,
    tag TEXT,            -- おすすめタグ
    description TEXT,
    image_file TEXT,
    FOREIGN KEY (maker_id) REFERENCES makers(id)
);

CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    flex TEXT,
    price INTEGER,
    weight INTEGER,
    length REAL,
    stock INTEGER DEFAULT 10,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- 3. メーカー登録
INSERT INTO makers (name, country) VALUES ('Taylormade', 'USA'), ('Callaway', 'USA'), ('PING', 'USA'), ('Titleist', 'USA');

-- 4. 商品登録 & 在庫登録 (価格も最新版)

-- --- ドライバー ---
INSERT INTO products (maker_id, name, club_type, tag, description, image_file) VALUES 
(1, 'Qi10 MAX', 'ドライバー', '初心者おすすめ', '慣性モーメント10000超えのやさしさ。', 'image01.jpg'),
(2, 'PARADYM Ai SMOKE', 'ドライバー', '中級者向け', 'AI設計フェースでミスに強い。', 'image02.jpg'),
(3, 'G430 MAX', 'ドライバー', '初心者おすすめ', 'ブレない飛距離。', 'image03.jpg');

INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name='Qi10 MAX'), 'S', 96800, 305, 45.25, 10),
((SELECT id FROM products WHERE name='PARADYM Ai SMOKE'), 'S', 86900, 300, 45.5, 5),
((SELECT id FROM products WHERE name='G430 MAX'), 'S', 93500, 302, 45.25, 10);

-- --- パター (価格未定問題を解消済み) ---
INSERT INTO products (maker_id, name, club_type, tag, description, image_file) VALUES 
(2, 'Odyssey Ai-ONE #1', 'パター', '全レベル対応', 'AI設計のインサートを搭載。芯を外してもボールスピードが落ちず、カップに届く。', 'image04.jpg'),
(1, 'Spider Tour X', 'パター', '中級者向け', 'ミスに強いスパイダーシリーズ。トラスホーゼルとの融合で安定性がさらに向上。', 'image05.jpg'),
(4, 'Super Select Newport 2', 'パター', 'アスリート向け', 'スコッティキャメロンの代名詞。削り出しヘッドによる極上の打感と美しい形状。', 'image06.jpg');

INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name='Odyssey Ai-ONE #1'), '-', 41580, 550, 34.0, 8),
((SELECT id FROM products WHERE name='Spider Tour X'), '-', 48400, 560, 34.0, 5),
((SELECT id FROM products WHERE name='Super Select Newport 2'), '-', 66000, 540, 34.0, 3);

-- --- フェアウェイウッド ---
INSERT INTO products (maker_id, name, club_type, tag, description, image_file) VALUES 
(3, 'G430 MAX FW', 'フェアウェイウッド', '初心者おすすめ', '「激飛」でおなじみ。とにかく曲がらず、球が上がりやすい安心感抜群のモデル。', 'image07.jpg'),
(1, 'Qi10 Tour FW', 'フェアウェイウッド', 'アスリート向け', 'ロフト調整機能付きで、操作性が高い。パワーヒッターが叩けるモデル。', 'image08.jpg'),
(2, 'PARADYM Ai SMOKE MAX FW', 'フェアウェイウッド', '全レベル対応', 'どこで打っても飛ぶAIフェース。ミスヒットに強く、多くのゴルファーに合う。', 'image09.jpg');

INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name='G430 MAX FW'), 'SR', 60500, 315, 43.0, 12),
((SELECT id FROM products WHERE name='Qi10 Tour FW'), 'S', 68200, 325, 42.0, 4),
((SELECT id FROM products WHERE name='PARADYM Ai SMOKE MAX FW'), 'R', 59400, 310, 43.25, 0);

-- --- アイアン (5本セット仕様) ---
INSERT INTO products (maker_id, name, club_type, tag, description, image_file) VALUES 
(1, 'P790 アイアン 5本セット', 'アイアン', '中級者向け', '【5本セット(#6-PW)】中空構造でカッコいいのにやさしくて飛ぶ。', 'image10.jpg'),
(4, 'T100 アイアン 5本セット', 'アイアン', 'アスリート向け', '【5本セット(#6-PW)】ツアープロ使用率No.1。正確な距離感と操作性を極めた軟鉄鍛造。', 'image11.jpg'),
(3, 'G430 アイアン 5本セット', 'アイアン', '初心者おすすめ', '【5本セット(#6-PW)】ダフっても滑ってくれるワイドソール。高弾道でグリーンに止まる。', 'image12.jpg');

INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name='P790 アイアン 5本セット'), 'S', 154000, 410, 37.0, 3),
((SELECT id FROM products WHERE name='T100 アイアン 5本セット'), 'S200', 154000, 430, 37.0, 2),
((SELECT id FROM products WHERE name='G430 アイアン 5本セット'), 'R', 121000, 370, 37.5, 5);

-- --- ウェッジ ---
INSERT INTO products (maker_id, name, club_type, tag, description, image_file) VALUES 
(4, 'Vokey SM10', 'ウェッジ', '全レベル対応', 'ウェッジの金字塔。多彩なグラインドでどんなライにも対応。', 'image13.jpg'),
(2, 'JAWS Raw', 'ウェッジ', '中級者向け', 'フェースのメッキを排除してスピン性能を最大化。強烈に止まる。', 'image14.jpg'),
(1, 'Milled Grind 4', 'ウェッジ', 'アスリート向け', '水に濡れてもスピンが落ちないレーザー加工。打感が柔らかい。', 'image15.jpg');

INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name='Vokey SM10'), 'S200', 27500, 460, 35.0, 20),
((SELECT id FROM products WHERE name='JAWS Raw'), 'S', 26400, 450, 35.25, 8),
((SELECT id FROM products WHERE name='Milled Grind 4'), 'S', 27500, 455, 35.0, 5);

"""

# ---------------------------------------------------------
# 実行
# ---------------------------------------------------------
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.executescript(sql)
    conn.commit()
    print(f"✨ データベースを完全リセット＆再構築しました！\n重複も解消され、全てのデータが最新の状態です。\n場所: {db_path}")
except sqlite3.Error as e:
    print(f"❌ エラーが発生しました: {e}")
finally:
    conn.close()