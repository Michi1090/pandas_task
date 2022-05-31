import mysql.connector
import pandas as pd
import subprocess as sub
import datetime

# DB接続
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='pandas_task'
)
cursor = conn.cursor()

# エクセルからデータ抽出
df = pd.read_excel('data.xlsx')

# ping実行〜DB登録
for i in range(len(df)):
    # 各データを変数に代入
    name = df.loc[i, 'name']
    url = df.loc[i, 'url']
    ip = df.loc[i, 'ip_address']
    today = datetime.datetime.today()
    dt = today.strftime('%Y-%m-%d %X')

    # pingコマンド実行
    res = sub.run(['ping', ip, '-c', '3', '-W', '1000'],
                  capture_output=True)
    print(res.stdout.decode('UTF-8'))

    # 結果の表示、及び格納
    if res.returncode == 0:
        print('成功\n')
        result = True
    else:
        print('失敗\n')
        result = False
    print("--------------------------------------------------------------")

    # DB登録
    cursor.execute(f'''
                   INSERT INTO pings
                   (name, url, ip_address, datetime, result)
                   VALUES ("{name}", "{url}", "{ip}", "{dt}", {result})
                   '''
                   )
    conn.commit()

# DB切断
cursor.close()
conn.close()
