import pandas as pd
import mysql.connector
from db.db import parameter

def load_sql_file(file) -> str:
    with open(file, "r") as fin:
        return fin.read()



if __name__ == "__main__":
    ret = load_sql_file("/home/work/mysql_server/command/mysql.sql")
    print(ret)


    # MySQLデータベースに接続
    db_connection = mysql.connector.connect(**parameter, ssl_disabled=True)

    # # SQLクエリを実行してデータを取得
    query = load_sql_file("/home/work/mysql_server/command/mysql.sql")    
    df = pd.read_sql(query, db_connection)

    # # ピボットテーブルを作成
    pivot_table = df.pivot_table(
        index=['collection_layer', 'datasource'],
        columns=["tactic", 'technique'],
        values='combination_count',
        aggfunc='max',
        fill_value=0
    )
    # # 必要に応じて、CSVなどのファイルに保存
    pivot_table.to_excel("to_excel.xlsx")

    # # データベース接続を閉じる
    db_connection.close()
