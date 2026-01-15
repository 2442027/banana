-- 1. タイトリスト（Titleist）をメーカーに追加（まだなければ）
INSERT OR IGNORE INTO makers (name, country) VALUES ('Titleist', 'USA');

-- 2. パターの商品データ（モデル）を追加
-- メーカーID: 1=Taylormade, 2=Callaway, 3=PING, 4=Titleist
INSERT INTO products (maker_id, name, club_type, description, image_file) VALUES 
(2, 'Odyssey Ai-ONE #1', 'パター', 'AI設計のインサートを搭載。芯を外してもボールスピードが落ちず、カップに届く。', 'image04.jpg'),
(1, 'Spider Tour X', 'パター', 'ミスに強いスパイダーシリーズ。トラスホーゼルとの融合で安定性がさらに向上。', 'image05.jpg'),
((SELECT id FROM makers WHERE name='Titleist'), 'Super Select Newport 2', 'パター', 'スコッティキャメロンの代名詞。削り出しヘッドによる極上の打感と美しい形状。', 'image06.jpg');

-- 3. 在庫スペックを追加
-- Flexはパターなので「-」表記にしています
INSERT INTO inventory (product_id, flex, price, weight, length, stock) VALUES 
((SELECT id FROM products WHERE name='Odyssey Ai-ONE #1'), '-', 41800, 550, 34.0, 8),
((SELECT id FROM products WHERE name='Spider Tour X'), '-', 46200, 560, 34.0, 5),
((SELECT id FROM products WHERE name='Super Select Newport 2'), '-', 66000, 540, 34.0, 3);