import pandas as pd
import mysql.connector
from db.db import parameter

def load_sql_file(file) -> str:
    with open(file, "r") as fin:
        return fin.read()
    
if __name__ == "__main__":
    db_connection = mysql.connector.connect(**parameter, ssl_disabled=True)

    query = load_sql_file("/home/work/mysql_server/command/mysql.sql")
    df = pd.read_sql(query, db_connection)
    df["combination_count"] = 1
    pivot_table = df.pivot_table(
        index=["tactic", 'technique'],
        columns=['collection_layer', 'datasource'],
        values='combination_count',
        aggfunc='max',
        fill_value=0
    )

    tech_url_dict_query = load_sql_file("/home/work/mysql_server/command/tech_url_dict.sql")
    technique_url_dic = pd.read_sql(tech_url_dict_query, db_connection).set_index("technique")["url"].to_dict()

    tac_order_dict = load_sql_file("/home/work/mysql_server/command/tac_order_dict.sql")
    tac_order_dic = pd.read_sql(tac_order_dict, db_connection).set_index("tactic")["sequence"].to_dict()


    pivot_table = pivot_table.reset_index()
    pivot_table["url"] = pivot_table["technique"].map(technique_url_dic)
    pivot_table["order"] = pivot_table["tactic"].map(tac_order_dic)

    pivot_table = pivot_table.set_index(["tactic", "technique"]).sort_values("order", ascending=True)
    pivot_table.to_excel("sample2.xlsx")






