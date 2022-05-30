import pandas as pd
from sqlalchemy import create_engine, false
import subprocess

# データベース接続
engine = create_engine('mysql://root:password@localhost:3306/pandas_task')

# エクセルからデータ抽出
df = pd.read_excel('data.xlsx')

# DBに登録〜IPアドレス抽出
with engine.begin() as con:
    df.to_sql('pings', con=con, if_exists='replace')
    ip = pd.read_sql('SELECT ip_address FROM pings', con=con)

print(ip)
for index, item in ip.iterrows():
    print(item['ip_address'])
