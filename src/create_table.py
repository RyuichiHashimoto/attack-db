from db.model import Tactics, TacTech, Techniques, TechData, Datasources, TacticOrders








if __name__ == "__main__":

    # DB.create_tables([Tactics, TacTech, Techniques, TechData, Datasources])
    # テーブルを作成
    for model in [TacticOrders]:
        model.create_table()
    
    # DB.create_tables()
    
    

    # データベース接続を閉じる
