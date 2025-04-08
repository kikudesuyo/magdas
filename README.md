# MAGDAS

## 環境構築

### 仮想環境の導入

仮想環境を有効化

`source .venv/bin/activate`

環境変数の登録

`.venv/bin/activate`にて`YOUR_PATH`を指定して下記を記述してください

```.sh
#環境変数を追加
export PYTHONPATH="YOUR_PATH/magdas/backend/src:$PYTHONPATH"
```
