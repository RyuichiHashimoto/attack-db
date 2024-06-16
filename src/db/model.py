from peewee import Model, CharField, DateField, BooleanField, MySQLDatabase, PrimaryKeyField, IntegerField
from db.db import DB

# 基本モデルクラス
class BaseModel(Model):
    class Meta:
        database = DB

    @classmethod
    def set_database(cls, database: MySQLDatabase) -> None:
        cls._meta.database = database

    

# tacticsモデル
class Tactics(BaseModel):
    tactic_id = CharField(primary_key=True, max_length=255)
    stix_id = CharField(null=False)
    name = CharField(null=False)
    description_en = CharField(null=False)
    description_jp = CharField(null=True)
    url = CharField(null=False)
    created = DateField(null=False)
    last_modified = DateField(null=False)
    domain = CharField(null=False)
    version = CharField(null=False)
    
class TacticOrders(BaseModel):
    tactic_id = CharField(primary_key=True, max_length=255)
    order = IntegerField()



# tac_techモデル
class TacTech(BaseModel):
    id = PrimaryKeyField()
    tactic_id = CharField()
    technique_id = CharField()

# techniquesモデル
class Techniques(BaseModel):
    technique_id = CharField(primary_key=True, max_length=255)
    stix_id = CharField()
    name = CharField()
    description_en = CharField()
    description_jp = CharField(null=True)
    url = CharField()
    created = DateField()
    last_modified = DateField()
    domain = CharField()
    version = CharField()
    detection = CharField()
    is_sub_technique = BooleanField()
    parent_technique = CharField(null=True)  # 親テクニックがない場合を考慮してnull許容

# tech_dataモデル
class TechData(BaseModel):
    id = PrimaryKeyField()
    datasource_id = CharField()
    technique_id = CharField()

# # tech_dataモデル
# class CollectionLayers(BaseModel):
#     layer_id = CharField(primary_key=True)
#     collectionlayer = CharField()
#     description_en = CharField(null=True)
#     description_jp = CharField(null=True)

# tac_techモデル
class DataCollection(BaseModel):
    id = PrimaryKeyField()
    datasource_id = CharField()
    collection_layer = CharField()
    


# datasourcesモデル
class Datasources(BaseModel):
    datasource_id = CharField(primary_key=True)
    datasource = CharField()
    stix_id = CharField()
    description_en = CharField()
    description_jp = CharField(null=True)
    # platform = CharField()
    created = DateField()
    last_modified = DateField()
    version = CharField()
    type = CharField(null=True)
    url = CharField(null=True)


