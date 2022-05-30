import pandas as pd
import mysql.connector as sql

# データベース接続
conn = sql.connect(
    host='localhost',
    port='3306',
    user='root',
    password='password',
    database='pandas_task'
)

# コネクションが切れた時に再接続してくれるよう設定
conn.ping(reconnect=True)

# エクセルからデータ抽出
df = pd.read_excel('data.xlsx')

# DBに登録
df.to_sql('pings', conn, if_exists='replace')

# データベース切断
conn.close()
