# orders

## 概要

受注データ集計デモ。

得意先マスタ・商品マスタ・受注履歴のグループ集計。


## 作業意図・目的
- SQL
  - 実務で行うクラウド上のデータ加工・集計処理をローカル環境（SQLite）で再現
- Python（pandas）
  - SQL処理を置き換えながらPython特有の記法やpandasについて学習
  - 学習補助として主にChatGPTを使用


## 作業工程・詳細

スプレッドシートで作成した元データを使用し、

- ピボットテーブル集計
- SQLite 集計
- Python（pandas）集計

をそれぞれ実装。

実務で行っていた Excel 集計、Access VBA、
Snowflake SQL による集計作業を参考に、
典型的な処理パターンを学習用に再構成したもの。

---


## folders

### PY
- Python（pandas）による集計処理ファイル一式

### SQL
- SQLite用のDBと集計処理ファイル一式

### CSV
- 元データCSV一式。スプレッドシートで作成し書き出したもの
- SQLite DBへの取込に使用
- Python集計の参照元
