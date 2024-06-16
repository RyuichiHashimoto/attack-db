from peewee import MySQLDatabase
from contextlib import contextmanager
from typing import Generator

parameter = {
    "database":  'miter-attack',  # データベース名
    "user":'hashimoto',  # ユーザー名
    "password":'hashimoto',  # パスワード
    "host":'miter-attack-db',  # ホスト名
    "port":3306  # ポート番号
}
DB = MySQLDatabase(**parameter)
DB.connect()
# def connect_to_DB()  -> Generator[MySQLDatabase, None, None]:
    
    

#     try:
#         yield DB
#     finally:
#         if not DB.is_closed():
#             DB.close()

