import pandas as pd
from pathlib import Path

# ディレクトリ指定
base_dir = Path(__file__).resolve().parent.parent

# CSV読み込む
orders = pd.read_csv(base_dir / "csv/T_orders.csv")
customers = pd.read_csv(base_dir / "csv/M_customers.csv")
products = pd.read_csv(base_dir / "csv/M_prod.csv")

# 得意先マスタと商品マスタを連結
df = orders.merge(customers, on="customer_id", how="left")
df = df.merge(products, on="product_id", how="left")

# 金額欄つくる
df["amount"] = df["quantity"] * df["unit_price"]

# 月集計用
df["order_date"] = pd.to_datetime(df["order_date"])

# 集計
result=(
    df.assign(month=pd.to_datetime(df["order_date"]).dt.to_period("M"))
    .groupby(["month", "region", "category"])
    .agg(
        odr_count=("customer_id", "count"),
        total_amount=("amount", "sum")
        )
    .reset_index()
)

result.to_csv("./PY/result.csv", index=False)

# # for test
print(result)

# # ディレクトリ確認
# print(base_dir)