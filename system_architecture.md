# システム構成図 (System Architecture)

Web 3層構造（Client, App Server, Database）を採用し、在庫管理システムと連動する構成としました。

```mermaid
graph TD
    User(("ユーザー<br/>(客/店長)"))
    
    subgraph Client ["Client Layer (Presentation)"]
        Browser["ブラウザ / スマホアプリ<br/>(UI表示・条件入力)"]
    end

    subgraph App ["Application Layer (Logic)"]
        Flask["Webサーバー<br/>Python (Flask)"]
        Logic{"ロジック判定"}
    end

    subgraph Data ["Data Layer (Persistence)"]
        DB[("データベース<br/>PostgreSQL")]
    end

    User --> Browser
    Browser -->|1.検索・購入| Flask
    Flask --> Logic
    Logic -->|2.在庫あり?| DB
    DB -->|3.データ返却| Flask
    Flask -->|4.表示・完了| Browser

    style Flask fill:#f9f,stroke:#333
    style DB fill:#ff9,stroke:#333
