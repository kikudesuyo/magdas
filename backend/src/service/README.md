# service ディレクトリ

アプリケーションのビジネスロジックを中心に実装しています。

---

## 🔄 EE-index の処理の流れ

以下の順で各種物理量の計算を行います。  
**全て UTC 時間で処理**し、必要に応じて `local_date` を指定します。

1. **H 成分の計算**

   - UTC ベースで地磁気 H 成分を計算します。

2. **ER（Electrojet Range）の計算**

   - H 成分を元に ER を算出します。

3. **EDst（Equatorial Disturbance Storm Time Index）の計算**

   - ER を用いて EDst を算出します。

4. **EUEL（Equatorial Upper Electrojet Level）の計算**

   - ER および EDst を元に EUEL を計算します。

5. **EEJ（Equatorial Electrojet）消失現象の検出**
   - EUEL を用いて EEJ の異常を検出します。
   - この処理のみ **ローカル日付（local_date）** を基に処理しますが、内部では UTC で計算します。

---
