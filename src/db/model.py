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
    tactic = CharField(null=False)
    description_en = CharField(null=False)
    description_jp = CharField(null=True)
    url = CharField(null=False)
    created = DateField(null=False)
    last_modified = DateField(null=False)
    domain = CharField(null=False)
    version = CharField(null=False)
    sequence = IntegerField(null=False, unique=True)

    # killchain
    killchain_id = CharField(max_length=255)
    
    
# tac_techモデル
class TacTech(BaseModel):
    id = PrimaryKeyField()
    tactic_id = CharField()
    technique_id = CharField()

# techniquesモデル
class Techniques(BaseModel):
    technique_id = CharField(primary_key=True, max_length=255)
    stix_id = CharField()
    technique = CharField()
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

class Cyberkillchain(BaseModel):
    killchain_id = CharField(primary_key=True, max_length=255)
    order = IntegerField()
    phase = CharField()
    description_en = CharField()
    description_jp = CharField(null=True)

    

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


# datasourcesモデル
class AdditionalDatasources(BaseModel):
    datasource_id = CharField(primary_key=True)
    is_target = IntegerField(default=False) # 0 使用しない、１　使用するかも　２　使用する。
    

class Mitigations(BaseModel):
    mitigation_id = CharField(primary_key=True)
    mitigation= CharField(null=False)
    description_en= CharField(null=False)
    description_jp= CharField(null=True)
    url= CharField(null=False)
    created = DateField()
    last_modified = DateField()
    domain= CharField(null=False)
    version= CharField(null=False)

class TechMitigations(BaseModel):
    id = PrimaryKeyField()
    mitigation_id = CharField()
    technique_id = CharField()


def update_additonal_data(datasource_id: str, new_value: int)  -> None:
    if type(new_value) is not int: raise TypeError
    if type(datasource_id) is not str: raise TypeError

    query = AdditionalDatasources.update(is_target=new_value).where(AdditionalDatasources.datasource_id == datasource_id)
    query.execute()
