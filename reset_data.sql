-- 既存の古いテーブルをすべて削除
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS makers;

-- 1. メーカーテーブルの作成
CREATE TABLE makers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    country TEXT
);

-- 2. 商品（モデル）テーブルの作成
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maker_id INTEGER,
    name TEXT NOT NULL,
    club_type TEXT,
    FOREIGN KEY (maker_id) REFERENCES makers(id)
);

-- 3. 在庫・スペック詳細テーブルの作成（エラーが出ていたのはこれ！）
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    flex TEXT,
    price INTEGER,
    weight INTEGER,
    length REAL,
    stock INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- テストデータの投入（ここを入れないと画面が真っ白になります）
INSERT INTO makers (name, country) VALUES ('Taylormade', 'USA');

INSERT INTO products (maker_id, name, club_type) VALUES (1, 'Qi35 MAX', 'ドライバー');

INSERT INTO inventory (product_id, flex, price, weight, length, stock) 
VALUES 
(1, 'S', 99000, 305, 45.25, 5),
(1, 'SR', 99000, 305, 45.25, 3),
(1, 'R', 99000, 305, 45.25, 0);