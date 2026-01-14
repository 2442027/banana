-- 既存のテーブルを削除
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS makers;

-- 1. メーカーテーブル
CREATE TABLE makers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    country TEXT
);

-- 2. 商品テーブル
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maker_id INTEGER,
    name TEXT NOT NULL,
    club_type TEXT,
    description TEXT,
    image_file TEXT,
    FOREIGN KEY (maker_id) REFERENCES makers(id)
);

-- 3. 在庫テーブル（デフォルトを10に設定）
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    flex TEXT,
    price INTEGER,
    weight INTEGER,
    length REAL,
    stock INTEGER DEFAULT 10, -- デフォルト値を10に設定
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- データ投入
INSERT INTO makers (name, country) VALUES ('Taylormade', 'USA'), ('Callaway', 'USA'), ('PING', 'USA');

INSERT INTO products (maker_id, name, club_type, description, image_file) VALUES 
(1, 'Qi10 MAX', 'ドライバー', '慣性モーメント10000超えのやさしさ。', 'image01.jpg'),
(2, 'PARADYM Ai SMOKE', 'ドライバー', 'AI設計フェースでミスに強い。', 'image02.jpg'),
(3, 'G430 MAX', 'ドライバー', 'ブレない飛距離。', 'image03.jpg');

-- 在庫データの投入
INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
(1, 'S', 99000, 305, 45.25, 10), -- デフォルト10個
(2, 'S', 88000, 300, 45.5, 5),   -- ★この商品を在庫5個（警告対象）に設定
(3, 'S', 93500, 302, 45.25, 10);