from pathlib import Path
import pandas as pd
import glob # ファイル読み込み

def get_prod_master():

    # ディレクトリ指定（実行ファイル基準）
    base_dir = Path(__file__).resolve().parent

    # CSVフォルダ指定
    csv_dir = Path(base_dir.parent / "CSV/for_PY/prod/")

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

        # データ内容確認用
        # print("ファイル名：", file)
        # print("行数" , df.shape[0])
        # print("列数" , df.shape[1])
        # print(df.head())



    ### data1:商品マスタAの加工
    df = data_list[0][1]
    df.rename(columns={
        "商品コード":"prod_cd",
        "商品カテゴリ":"category",
        "商品名":"prod_nm",
        "単価":"unit_price"
        },
        inplace=True
    )
    df["prod_cd"]= "AAA" + df["prod_cd"].astype(str).str.zfill(5)
    df1=df

    ### data2:商品マスタBの加工
    df = data_list[1][1]
    df = (
        # ラベル行をはずす、商品コード列は正規表現で英数のみ。import re不要
        df[df["商品コード"].str.match(r"^[A-Z0-9]+$", na=False)].copy()
        # カラム名設定
        .rename(columns={
            "商品コード":"prod_cd",
            "商品名":"prod_nm",
            "単価":"unit_price",
            "更新日":"update"
            },
        )
        # カテゴリ列設定（このCSVファイルはすべて商品カテゴリBBB想定）
        .assign(category="BBB")
    )
    last_rec=(
        # 更新日が最新のレコードのみ採用
        df.sort_values("update")
        .groupby("prod_cd")
        .tail(1)
        [["prod_cd","category","prod_nm","unit_price"]]
    )
    df2=last_rec


    ### data3:商品マスタCの加工
    df = data_list[2][1]
    df=(
        # カラム名設定
        df.rename(columns={
            "product code":"prod_cd",
            "product group":"prod_gr",
            "product name":"prod_nm",
            "unit price":"unit_price"
        })
    )
    # product groupに商品名をカテゴリがまとめて入っているので切り分けてそれぞれのカラムに格納
    df[["prod_nm", "category"]] = (
        df["prod_gr"]
        .str.replace("】", "", regex=False)
        .str.split("【", expand=True)
    )
    # 外貨単価にレートをかけて日本円単価にする。
    # 四捨五入して整数にする  
    df["unit_price"]=(df["unit_price"]*df["rate"]).round(0).astype(int)

    # 加工後の必要項目のみ呼び出し
    df3=df[["prod_cd","category","prod_nm","unit_price"]]

    # 3つの加工済み商品マスタを連結
    df=pd.concat([df1, df2, df3], ignore_index=True)

    # 単価を数値にしておく
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    result=df

    # print(result)

    return result
