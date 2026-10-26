# 4. フロントエンド詳細 (Frontend)

Frontend は **React** と **TypeScript** で構築され、ビルドツールに **Vite** を使用しています。

## ディレクトリ構成 (`frontend/src`)

```
frontend/src
├── components  # 再利用可能な UI コンポーネント
├── hooks       # カスタムフック
├── pages       # 各ページごとのコンポーネント
├── utils       # ユーティリティ関数
├── types       # TypeScript 型定義
├── App.tsx     # メインアプリケーションコンポーネント (ルーティング定義など)
└── mains.tsx   # エントリポイント
```

## 技術スタック詳細

- **React Config**: `vite.config.ts` で設定。プロキシ設定などはここで確認できます。
- **Styling**: `Tailwind CSS` を使用。`tailwind.config.js` でテーマ設定が可能です。
- **State Management**: `Zustand` を用いて、グローバルな状態（選択された期間、データのキャッシュなど）を管理しています。
- **HTTP Client**: `Axios` を使用して Backend API と通信します。
- **Data Visualization**: `react-chartjs-2` (Chart.js wrapper) を使用して、時系列データである EE-index などをグラフ描画します。

## 開発フロー

1.  `npm run dev` でローカルサーバーを起動。
2.  `src/components` や `src/pages` を編集。HMR (Hot Module Replacement) により即座に反映されます。
3.  API リクエスト部分は `Axios` インスタンスの設定や、カスタムフック内で管理されています。

## 主要コンポーネント

- **Sidebar**: ナビゲーションや設定項目を表示するサイドバー。
- **DataSelector**: データ取得のためのパラメータ（期間、観測所など）を選択するコンポーネント。
- **Charts**: 取得したデータを描画するグラフコンポーネント群。

[目次に戻る](./00_index.md)
