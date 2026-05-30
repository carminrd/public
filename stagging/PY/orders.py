from pathlib import Path
import pandas as pd
import glob # ファイル読み込み


def get_orders_tbl():
    # ディレクトリ指定（実行ファイル基準）
    base_dir = Path(__file__).resolve().parent

    # CSVフォルダ指定
    csv_dir = Path(base_dir.parent / "CSV/for_PY/odr/")

    # CSVファイルリスト
    csv_files = list(csv_dir.glob("*.csv"))

    # リストつくる
    data_list = []

    for file in csv_files:
        # print(f"読み込み: {file.name}")

        df = pd.read_csv(file)

        file=Path(file).name
        
        #パスなしファイル名とdataflameをリストに保存 
        data_list.append([file, df])



    # データ内容確認
    # file_name, df = data_list[0]
    # print("ファイル名：", file_name)
    # print("行数" , df.shape[0])
    # print("列数" , df.shape[1])
    # print(df.head())



    ### data1:orders
    df = data_list[0][1]
    # カラム名変更
    df.rename(columns={
        "オーダーID":"order_no",
        "オーダーID枝番":"order_seq",
        "受付日":"order_date",
        "得意先コード":"cust_cd",
        "商品コード":"prod_cd",
        "ステータス":"status",
        "数量":"quantity"
        },
        inplace=True
    )
    # 数量を数値にしておく
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    # オーダーIDごとの最終レコードステータス・日付を取得
    last_odr = (
        df.sort_values("order_date")
        .groupby("order_no")
        .tail(1)
        [["order_no","order_date","status"]]
        .rename(columns={
            "status": "last_status",
            "order_date": "update"
        })
    )
    # 受注レコードに連結
    orders = (
        df[df["status"] == "受注"]
        [["order_no","order_date","cust_cd","prod_cd","quantity"]].copy()
        .merge(last_odr, on="order_no", how="left")
    )
    result=orders
    # print(result)

    return result
