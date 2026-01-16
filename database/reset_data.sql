DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS makers;

-- 1. メーカーテーブル
CREATE TABLE makers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    country TEXT
);

-- 2. 商品テーブル (★ tag カラムを追加)
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maker_id INTEGER,
    name TEXT NOT NULL,
    club_type TEXT,
    tag TEXT,            -- '初心者おすすめ', '中級者向け', 'アスリート向け' など
    description TEXT,
    image_file TEXT,
    FOREIGN KEY (maker_id) REFERENCES makers(id)
);

-- 3. 在庫テーブル
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

-- データ投入
INSERT INTO makers (name, country) VALUES ('Taylormade', 'USA'), ('Callaway', 'USA'), ('PING', 'USA'), ('Titleist', 'USA');

-- 商品データ (★ tag を追加)
INSERT INTO products (maker_id, name, club_type, tag, description, image_file) VALUES 
(1, 'Qi10 MAX', 'ドライバー', '初心者おすすめ', '慣性モーメント10000超えのやさしさ。', 'image01.jpg'),
(2, 'PARADYM Ai SMOKE', 'ドライバー', '中級者向け', 'AI設計フェースでミスに強い。', 'image02.jpg'),
(3, 'G430 MAX', 'ドライバー', '初心者おすすめ', 'ブレない飛距離。', 'image03.jpg'),
(2, 'Odyssey Ai-ONE #1', 'パター', '全レベル対応', 'AI設計のインサートを搭載。', 'image04.jpg'),
(1, 'Spider Tour X', 'パター', '中級者向け', 'ミスに強いスパイダーシリーズ。', 'image05.jpg'),
(4, 'Super Select Newport 2', 'パター', 'アスリート向け', '削り出しヘッドによる極上の打感。', 'image06.jpg');

-- 在庫データ
INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
(1, 'S', 99000, 305, 45.25, 10),
(2, 'S', 88000, 300, 45.5, 5),
(3, 'S', 93500, 302, 45.25, 10),
(4, '-', 41800, 550, 34.0, 8),
(5, '-', 46200, 560, 34.0, 5),
(6, '-', 66000, 540, 34.0, 3);