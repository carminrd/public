from pathlib import Path
import pandas as pd
import glob # ファイル読み込み
import numpy as np

def get_cust_master():

    # ディレクトリ指定（実行ファイル基準）
    base_dir = Path(__file__).resolve().parent

    # CSVフォルダ指定
    csv_dir = Path(base_dir.parent / "CSV/for_PY/cust/")

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



    ### data1:得意先マスタASの加工
    df = data_list[0][1]
    # カラム名をつける
    df=(df.rename(columns={
        "得意先コード":"cust_cd",
        "得意先名称":"cust_nm",
        "更新日":"update",
        "国":"country"
        })
    )
    last_rec=(
        # 更新日が最新のレコードのみ採用
        df.sort_values("update")
        .groupby("cust_cd")
        .tail(1)
        [["cust_cd","cust_nm","country"]]
        # エリアASを追加：当CSVファイルはすべてASエリア想定
        .assign(area="AS")
    )
    df1=last_rec

    ### data2:得意先マスタEUの加工
    df = data_list[1][1]
    # カラム名をつける
    df=(df.rename(columns={
        "得意先コード":"cust_cd",
        "得意先名称":"cust_nm",
        "更新日":"update",
        "国":"country"
        })
        # エリアEUを追加：当CSVファイルはすべてEUエリア想定
        .assign(area="EU")
        # 更新日カラムを除外（重複なしデータ想定）
        .drop(columns=["update"])
    )
    df2=df

    ### data3:得意先マスタNAの加工
    df = data_list[2][1]
    # カラム名修正
    df=(df.rename(columns={
        "customer_code":"cust_cd",
        "customer_name":"cust_nm",
        })
    )
    # areaの空欄埋め
    df["area"] = np.where(
        df["area"].isna(),
        np.where(df["country"] == "USA", "NA", "SA"),
        df["area"]
        )
    df3=df[["cust_cd","cust_nm","country","area"]]

    # 3つの加工済み得意先マスタを連結
    result=pd.concat([df1, df2, df3], ignore_index=True)

    return result
