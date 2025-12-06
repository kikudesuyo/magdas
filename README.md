# MAGDAS

本プロジェクトは、九州大学国際宇宙惑星環境研究センターが提供する

## リポジトリ構成

- backend: バックエンド (API サーバー、データベース、統計解析)
- frontend: フロントエンド (ユーザーインターフェース)

## 環境構築

本プロジェクトの backend では uv を使用しています。

#### 1. uv のインストール

```bash
brew install uv
```

#### 2. ライブラリのインストール

```bash
make init
```

## 開発サーバー起動

### ローカル環境での開発

#### バックエンド

```bash
make be-dev
```

#### フロントエンド

```bash
make fe-dev
```

### Docker 環境

```
make up
```

## 統計解析を行う場合

統計解析関連の操作は backend ディレクトリで行います。

```bash
cd backend
```

詳細は `backend/README.md` を参照してください
