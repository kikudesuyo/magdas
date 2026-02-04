# 1. システム概要 (Overview)

## プロジェクトの目的

MAGDAS (Magnetic Data Acquisition System) ネットワークから取得された地磁気データを解析し、特に **EE-index (Equatorial Electrojet index)** の算出と可視化を行うことを目的としています。研究者がブラウザ上で手軽にデータの期間を指定し、プロットを確認したりデータをダウンロードしたりできる環境を提供します。

## 主要機能 (Features)

本システムが提供する主な機能は以下の通りです。

### 1. EE-index の時系列表示 (Real-time Display)

観測点および期間を指定して、EE-index をブラウザ上でグラフ表示します。

- **期間指定**: 任意の期間（1日、数日、1ヶ月など）を選択可能。
- **観測点**: 複数の観測点のデータを切り替えて表示。
- **インタラクティブな操作**: グラフの拡大・縮小や値の確認が可能。

### 2. 特異型 EEJ の検知 (Peculiar EEJ Detection)

ペルー・ブラジル領域等における特異型 EEJ (Equatorial Electrojet) 現象を検知し、表示します。

- グラフ上で特異日が視覚的に確認可能。

### 3. MAGDAS 観測データのダウンロード

指定した期間の EE-index データをファイルとしてダウンロードできます。

- **フォーマット**: .iaga 形式 (IAGA-2002 format に準拠)
- **圧縮**: 複数日のデータをまとめて ZIP ファイルとして提供。

## 技術スタック

### フロントエンド (Frontend)

ユーザーインターフェースを提供します。

- **Language**: TypeScript
- **Framework**: React
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Routing**: React Router
- **Visualization**: Chart.js (react-chartjs-2)
- **HTTP Client**: Axios

### バックエンド (Backend)

API サーバーおよびデータ処理を担います。

- **Language**: Python
- **Framework**: FastAPI (ASGI Server: Uvicorn)
- **Package Manager**: uv
- **Task Runner**: invoke (tasks.py), Makefile
- **Architecture**: Layered Architecture (Handler, Usecase, Service, Domain)

### インフラ・環境 (Infrastructure)

- **Containerization**: Docker, Docker Compose
- **Data Storage**: ローカルファイルシステム (`Storage` ディレクトリ配下の `.mgd` ファイルおよび CSV)

## アーキテクチャ概要

本システムは、REST API ベースのクライアント・サーバー構成を採用しています。

1.  **Frontend**: ユーザーからの入力を受け付け、バックエンド API にデータリクエストを送信します。取得したデータをグラフ描画ライブラリを用いて可視化します。
2.  **Backend**: リクエストを受け取り、`Storage` ディレクトリ内の地磁気データファイル (.mgd) を読み込み・解析・加工して JSON 形式または ZIP ファイルで返却します。
3.  **Data**: データはファイルシステム上で管理され、ディレクトリ構造 (`Storage/magdas/...`) に基づいてアクセスされます。

次章: [環境構築・セットアップ](./02_setup.md)
