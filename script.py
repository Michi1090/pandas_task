from email import charset
import mysql.connector
import pandas as pd
import subprocess as sub
import datetime
import logging

# DB接続
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='pandas_task',
    charset = 'utf8'
)
cursor = conn.cursor()

# トランザクションスタート
# ===========================================================

# 実行日時を生成
dt = datetime.datetime.today()
table_name = dt.strftime('%Y_%m_%d %X')

# エクセルからマスタ取得
df = pd.read_excel('data.xlsx')

# ===========================================================

# テーブルの作成
cursor.execute(f'''
                CREATE TABLE `{table_name}` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(30),
                    url VARCHAR(100),
                    ip_address VARCHAR(30),
                    result BOOLEAN
                );
              ''')

# 監視対象をDBに登録
for i in range(len(df)):
    # 各データを変数に代入
    name = df.loc[i, 'name']
    url = df.loc[i, 'url']
    ip = df.loc[i, 'ip_address']

    # SQL発行
    cursor.execute(f'''
                    INSERT INTO `{table_name}`
                    (name, url, ip_address)
                    VALUES ('{name}', '{url}', '{ip}')
                  ''')

# DBへコミット
conn.commit()

# ==================================================================

# ping実行〜結果をDBに登録
# IPアドレスをDBより抽出
cursor.execute(f'SELECT ip_address FROM {table_name}')

for ping_ip in cursor:

    # pingコマンド実行
    res = sub.run(
                    ['ping', ping_ip, '-c', '3', '-W', '1000'],
                    capture_output=True,
                    shell=True
                )
    print(res.stdout.decode('UTF-8'))

    # 結果の表示、及び格納
    if res.returncode == 0:
        print('成功\n')
        result = True
    else:
        print('失敗\n')
        result = False
    print("--------------------------------------------------------------")

    # SQL発行
    cursor.execute(f'''
                   UPDATE FROM {table_name}
                   SET result = {result}
                   WHERE ip_address = '{ping_ip}'
                   ''')


# DB登録
conn.commit()

# =================================================================

# トランザクション終了

# DB切断
cursor.close()
conn.close()

# # ログ出力の設定
# logging.basicConfig(
#     filename='test.log',
#     level=logging.DEBUG,
#     format='[%(asctime)s](%(levelname)s) filename=%(filename)s(%(lineno)s): %(message)s',
#     datefmt='%Y/%m/%d %H:%M:%S',
# )
# logging.error('ログを出力しました。')
