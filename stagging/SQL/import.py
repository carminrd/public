import pandas as pd
import sqlite3
from pathlib import Path

# ディレクトリ指定（実行ファイル基準）
base_dir = Path(__file__).resolve().parent

# SQLite接続（ファイル自動作成）
conn = sqlite3.connect(base_dir / "rowdata.db")


# SQLiteに書き込み：CSVフォルダ下のcsvファイル対象、ファイル名ヘッダ半角スペースとハイフン処理
for csv_file in Path(base_dir.parent / "CSV/").rglob("*.csv"):
    table_name = csv_file.stem.replace(" ", "").replace("-", "_")

    print(csv_file, "->", table_name)

    df = pd.read_csv(csv_file, dtype=str)
    df.columns = df.columns.str.replace(" ", "_")
    df.to_sql(table_name, conn, if_exists="replace", index=False)

conn.commit()
conn.close()
