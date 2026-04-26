import pandas as pd
import sqlite3
from pathlib import Path

# ディレクトリ指定（実行ファイル基準）
base_dir = Path(__file__).resolve().parent

# SQLite接続（ファイル自動作成）
conn = sqlite3.connect(base_dir / "orders.db")

# CSV読み込み：親フォルダ＞csv
orders = pd.read_csv(base_dir.parent / "csv/T_orders.csv")
customers = pd.read_csv(base_dir.parent / "csv/M_customers.csv")
products = pd.read_csv(base_dir.parent / "csv/M_prod.csv")

# SQLiteに書き込み
orders.to_sql("T_orders", conn, if_exists="replace", index=False)
customers.to_sql("M_customers", conn, if_exists="replace", index=False)
products.to_sql("M_prod", conn, if_exists="replace", index=False)

conn.close()

# # for test
# import os
# print(os.getcwd())