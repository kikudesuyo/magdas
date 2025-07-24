# service ディレクトリ

アプリケーションのビジネスロジックを中心に実装しています。

**EEJ（Equatorial Electrojet）消失現象の検出**

- EUEL を用いて EEJ の異常を検出します。
- この処理のみ **ローカル日付（local_date）** を基に処理しますが、内部では UTC で計算しています。
