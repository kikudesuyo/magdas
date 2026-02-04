# 2. 環境構築・セットアップ (Setup)

本プロジェクトの開発および実行に必要な環境構築手順を説明します。

## 前提条件 (Prerequisites)

以下のツールがインストールされていることを確認してください。

- **Git**
- **Docker** & **Docker Compose** (Docker Desktop 等)
- **Node.js** (v20以上推奨)
- **Python** (v3.10以上推奨)
- **Homebrew** (macOS の場合)

## インストール手順 (Installation)

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd magdas
```

### 2. パッケージマネージャー `uv` のインストール

Backend のパッケージ管理には `uv` を使用しています。

```bash
brew install uv
```

### 3. 先行セットアップ

依存ライブラリのインストールなどの初期化を行います。

```bash
make init
# 内部的に `backend` で `uv sync`、`frontend` で `npm install` が実行されます。
```

## 開発サーバーの起動 (Running the App)

### Docker 環境での起動 (推奨)

Docker Compose を使用して Frontend と Backend を一括で起動します。

```bash
make up
```

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend API: `http://localhost:8000` (または設定されたポート)

停止する場合:

```bash
make down
```

### ローカル環境での個別起動

Frontend と Backend を個別に起動して開発を行う場合の手順です。

#### Backend

```bash
make be-dev
# または
cd backend && uv run inv server
```

これにより、自動リロード(hot relaod)有効な状態で FastAPI サーバーが起動します。

#### Frontend

```bash
make fe-dev
# または
cd frontend && npm run dev
```

Vite サーバーが起動します。

## データの準備

本システムは `backend/Storage` ディレクトリ内の地磁気データファイル (.mgd) を参照します。
ローカル開発時は、適切なディレクトリ構造で配置する必要があります (例: `backend/Storage/magdas/AAB/Min/1999/...`)。
詳細は `backend/README.md` を参照するか、管理者にお問い合わせください。

次章: [バックエンド詳細](./03_backend.md)
