import os
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/ipl")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
files = {
    "matches": os.path.join(BASE_DIR, "matches.csv"),
    "deliveries": os.path.join(BASE_DIR, "deliveries.csv"),
}

for table, path in files.items():
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df.to_sql(table, engine, if_exists="replace", index=False, chunksize=20000)
    print(table, df.shape)