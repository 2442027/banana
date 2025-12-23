# システム構成図 (System Architecture)

Web 3層構造（Client, App Server, Database）を採用し、在庫管理システムと連動する構成としました。

```mermaid
graph TD
    %% ノードの定義
    User((ユーザー<br/>客/店長))
    
    subgraph "Client Layer (Presentation)"
        Browser[ブラウザ / スマホアプリ<br/>UI表示・条件入力]
    end

    subgraph "Application Layer (Logic)"
        Flask[Webサーバー<br/>Python (Flask)]
        Logic{ロジック判定}
    end

    subgraph "Data Layer (Persistence)"
        DB[(データベース<br/>PostgreSQL)]
    end

    %% フローの定義
    User -->|アクセス| Browser
    Browser -->|1. 検索条件・購入リクエスト| Flask
    
    Flask --> Logic
    Logic -->|2. 在庫数チェック (Stock > 0)| DB
    
    DB -->|3. 商品データ返却| Flask
    Flask -->|4. おすすめ商品表示 / 購入完了| Browser

    %% スタイル調整（見やすくするため）
    style Flask fill:#f9f,stroke:#333,stroke-width:2px
    style DB fill:#ff9,stroke:#333,stroke-width:2px
