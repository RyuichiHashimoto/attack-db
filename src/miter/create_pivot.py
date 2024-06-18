import pandas as pd
import mysql.connector
from db.db import parameter

if __name__ == "__main__":


    # MySQLデータベースに接続
    db_connection = mysql.connector.connect(**parameter, ssl_disabled=True)

    # SQLクエリを実行してデータを取得
    query = '''
    SELECT datasource, technique, COUNT(*) as combination_count
    FROM techdata td
    LEFT JOIN datasources ds ON ds.datasource_id = td.datasource_id
    LEFT JOIN techniques t ON t.technique_id = td.technique_id
    GROUP BY td.datasource_id, td.technique_id
    '''
    df = pd.read_sql(query, db_connection)

    # ピボットテーブルを作成
    pivot_table = df.pivot_table(
        index='datasource',
        columns='technique',
        values='combination_count',
        fill_value=0
    )
    # 必要に応じて、CSVなどのファイルに保存
    pivot_table.to_csv('pivot_table.csv')

    # データベース接続を閉じる
    db_connection.close()
