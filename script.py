import pandas as pd
from sqlalchemy import create_engine

# データベース接続
engine = create_engine('mysql://root:password@localhost:3306/pandas_task')

# エクセルからデータ抽出
df = pd.read_excel('data.xlsx')

# DBに登録
with engine.begin() as con:
    df.to_sql('pings', con=con, if_exists='replace', index=False)

# データベース切断
con.close()
