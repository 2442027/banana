-- 1. 商品テーブルを作成（まだなければ作る）
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    maker TEXT,
    price INTEGER,
    weight INTEGER,
    length REAL,
    flex TEXT,
    stock INTEGER
);

-- 2. データを登録（S, SR, R の3行分）
INSERT INTO products (name, maker, price, weight, length, flex, stock) VALUES 
('テーラーメイド Qi35 MAX メンズ ドライバー Diamana BLUE TM50 シャフト 2025', 'Taylormade', 99000, 305, 45.25, 'S', 5),
('テーラーメイド Qi35 MAX メンズ ドライバー Diamana BLUE TM50 シャフト 2025', 'Taylormade', 99000, 305, 45.25, 'SR', 3),
('テーラーメイド Qi35 MAX メンズ ドライバー Diamana BLUE TM50 シャフト 2025', 'Taylormade', 99000, 305, 45.25, 'R', 0);

-- 3. ちゃんと入ったか確認
SELECT * FROM products;