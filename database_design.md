# データベース設計書 (ゴルフクラブ専門店)

## 1. テーブル定義・ER図
正規化を行い、メーカー(Brands)とカテゴリ(Categories)を分離しました。

```mermaid
erDiagram
    BRANDS ||--|{ CLUBS : "makes"
    CATEGORIES ||--|{ CLUBS : "categorizes"
    CLUBS ||--o{ SALES : "sold as"

    BRANDS {
        int id PK
        string name "メーカー名"
    }

    CATEGORIES {
        int id PK
        string name "種類"
    }

    CLUBS {
        int id PK "主キー"
        string name "商品名"
        int price "価格"
        int stock_quantity "在庫数 (Check >= 0)"
        int brand_id FK "外部キー"
        int category_id FK "外部キー"
    }

    SALES {
        int id PK
        int club_id FK
        timestamp sold_at "販売日時"
    }
