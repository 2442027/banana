# データベース設計書 (ゴルフクラブ専門店)

## [cite_start]1. ER図・テーブル定義 [cite: 19, 253]
正規化を行い、メーカー(Brands)とカテゴリ(Categories)を分離しました。

### Clubs (商品テーブル)
- **id**: INT, PK, Auto Increment
- **name**: VARCHAR(100) (商品名)
- **price**: INT
- [cite_start]**stock_quantity**: INT (Check >= 0) ※在庫は0以上 [cite: 251]
- **brand_id**: INT, FK (Brandsテーブル参照)
- **category_id**: INT, FK (Categoriesテーブル参照)

### Brands (メーカーテーブル)
- **id**: INT, PK
- **name**: VARCHAR(50) (例: TaylorMade)

## [cite_start]2. トランザクション設計 [cite: 250]
購入時は「売上記録」と「在庫減少」を同時に行います。
1. `BEGIN`
2. `INSERT INTO sales ...`
3. `UPDATE clubs SET stock_quantity = stock_quantity - 1 ...`
4. `COMMIT`

## [cite_start]3. SQLサンプル (Join/副文) [cite: 251]
- **Join:** 商品名と一緒にメーカー名を表示する。
  `SELECT c.name, b.name FROM clubs c JOIN brands b ON c.brand_id = b.id;`
- **Subquery:** 平均価格以上の商品を探す。
  `SELECT * FROM clubs WHERE price > (SELECT AVG(price) FROM clubs);`
