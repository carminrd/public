from pathlib import Path
import pandas as pd

# 他ファイルで作ったモジュールを読み込み
from orders import get_orders_tbl as orders
from products import get_prod_master as products
from customers import get_cust_master as customers

df=orders()
prod=products()
cust=customers()

# 得意先マスタと商品マスタを連結
df = df.merge(cust, on="cust_cd", how="left")
df = df.merge(prod, on="prod_cd", how="left")

# 金額欄つくる
df["amount"] = (df["quantity"] * df["unit_price"])

# 月集計用
df["order_date"] = pd.to_datetime(df["order_date"])

# 集計
result=(
    df.assign(month=pd.to_datetime(df["order_date"]).dt.to_period("M"))
    .groupby(["month", "area", "category"])
    .agg(
        odr_count=("cust_cd", "count"),
        total_amount=("amount", "sum")
        )
    .reset_index()
)
# print(result)


result.to_csv("./result.csv", index=False)


