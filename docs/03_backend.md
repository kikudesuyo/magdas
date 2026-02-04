# 3. バックエンド詳細 (Backend)

Backend は **FastAPI** を用いて構築されており、Layered Architecture に基づいた設計になっています。

## ディレクトリ構成 (`backend/src`)

```
backend
├── src
│   ├── domain      # ドメインロジック・エンティティ
│   ├── service     # ビジネスロジック
│   ├── usecase     # アプリケーション固有のユースケース
│   ├── handler     # APIハンドラ (Controller)
│   ├── repository  # データアクセス層
│   ├── routes.py   # API ルーティング定義
│   └── main.py     # アプリケーションエントリポイント
├── Storage         # データファイル置き場 (.mgd, .csv)
├── tasks.py        # invoke タスク定義
└── pyproject.toml  # 依存関係定義 (uv)
```

## アーキテクチャ設計

機能間の結合度を下げ、テスト容易性と保守性を高めるために以下のレイヤー構造を採用しています。

1.  **Handler Layer (`src/handler`)**:
    - HTTP リクエストを受け取り、バリデーションを行った後、Usecase 層を呼び出します。
    - レスポンスの整形を担当します。
    - 原則として1つのハンドラにつき1つのファイルを作成します (`_handler` サフィックス)。

2.  **Usecase Layer (`src/usecase`)**:
    - 特定のユースケース（例: 「期間指定でEE-indexを取得する」）を実現するために、複数の Service を調整します。

3.  **Service Layer (`src/service`)**:
    - 具体的なビジネスロジックや計算処理を実装します。

4.  **Domain Layer (`src/domain`)**:
    - ドメインオブジェクトや定数などを定義します。

## 主要機能と API エンドポイント

`src/routes.py` に定義されています。

- **GET `/ee-index`**: 指定期間の EE-index データを取得します。
- **GET `/eej`**: EEJ (Equatorial Electrojet) データを取得します。
- **GET `/download/ee-index/by-days`**: 日単位で EE-index データを ZIP 形式でダウンロードします。
- **GET `/download/ee-index/by-range`**: 範囲指定で EE-index データを ZIP 形式でダウンロードします。

## タスクランナー (Invoke)

`tasks.py` に定義されたコマンドを `uv run inv <task_name>` で実行できます。

- `server`: 開発用サーバーを起動します。
- `test <filename>`: 指定したテストファイルを実行します。
- `test-all`: 全てのテストを実行します。

## データ管理

データは `Storage` ディレクトリ以下に格納されます。

- **MAGDAS Data**: `.mgd` 形式のバイナリデータ。
- **KP Data**: `Storage/ee_idex/kpdata.csv` など。

開発時にはこのディレクトリに必要な生データを配置する必要があります。

次章: [フロントエンド詳細](./04_frontend.md)
