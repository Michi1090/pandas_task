import pandas as pd
from sqlalchemy import create_engine, true
import subprocess as sub

# データベース接続
engine = create_engine('mysql://root:password@localhost:3306/pandas_task')

# エクセルからデータ抽出
df = pd.read_excel('data.xlsx')

# DBに登録〜IPアドレス抽出
with engine.begin() as con:
    df.to_sql('pings', con=con, if_exists='replace')
    ip = pd.read_sql('SELECT ip_address FROM pings', con=con)

    # DBから個別のIPアドレス抽出〜結果をDBへ格納
    for index, item in ip.iterrows():
        # 各IPアドレスごとにpingコマンドを実行
        res = sub.run(['ping', item['ip_address'], '-c', '3', '-W', '1000'],
                    capture_output=True)
        print(res.stdout.decode('UTF-8'))

        # pingコマンド成功時は0、失敗時はそれ以外を返す
        if res.returncode == 0:
            print('成功\n\n')
        else:
            print('失敗\n\n')
        print("--------------------------------------------------------------")
