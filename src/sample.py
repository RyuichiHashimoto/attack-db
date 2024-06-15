from peewee import *
import pymysql

# MySQLデータベースに接続
db = MySQLDatabase(
    'miter-attack',  # データベース名
    user='hashimoto',  # ユーザー名
    password='hashimoto',  # パスワード
    host='miter-attack-db',  # ホスト名
    port=3306  # ポート番号
)

# 基本モデルクラス
class BaseModel(Model):
    class Meta:
        database = db

# サンプルテーブルモデル
class User(BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    join_date = DateTimeField()

# テーブルを作成
db.connect()
db.create_tables([User])

# サンプルデータを挿入
user = User.create(username='', email='john@example.com', join_date='2024-06-16 00:00:00')
user.save()

# データをクエリして表示
for user in User.select():
    print(f'Username: {user.username}, Email: {user.email}, Join Date: {user.join_date}')

# データベース接続を閉じる
db.close()
