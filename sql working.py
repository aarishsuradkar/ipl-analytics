import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/ipl")

files = {
    "matches": r"C:\Users\SCI\Desktop\data analyst\ipl-analytics\matches.csv",
    "deliveries": r"C:\Users\SCI\Desktop\data analyst\ipl-analytics\deliveries.csv",
}

for table, path in files.items():
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df.to_sql(table, engine, if_exists="replace", index=False, chunksize=20000)
    print(table, df.shape)