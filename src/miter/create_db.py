import polars as pl
from peewee import Model

Record = dict[str, float|int|str| None]

COLUMN_MAPPING_TACTICS = {
    "ID": "tactic_id",
    "STIX ID": "stix_id",
    "name": "tactic",
    "description": "description_en",
    "url": "url",
    "created": "created",
    "last modified": "last_modified",
    "domain": "domain",
    "version": "version"
}

COLUMN_MAPPING_TECHNIQUE = {
    "ID": "technique_id",
    "STIX ID": "stix_id",
    "name": "technique",
    "description": "description_en",
    "url": "url",
    "created": "created",
    "last modified": "last_modified",
    "domain": "domain",
    "version": "version",
    "detection": "detection",
    "is sub-technique": "is_sub_technique",
    "sub-technique of": "parent_technique"
}

COLUMN_MAPPING_DATASOURCE = {    
    "name": "datasource",
    "ID": "datasource_id",
    "STIX ID": "stix_id",
    "description": "description_en",
    # "platforms": "platforms",
    "created": "created",
    "modified": "last_modified",
    "type": "type",
    "version": "version",
    "url": "url"
}

TACTIC_ORDER_DICT = {
    "TA0001": 3,    
    "TA0002": 4,
    "TA0003": 5,
    "TA0004": 6,
    "TA0005": 7,
    "TA0006": 8,
    "TA0007": 9,
    "TA0008": 10,
    "TA0009": 11,
    "TA0010": 12,
    "TA0011": 13,
    "TA0040": 14,
    "TA0042": 2,
    "TA0043": 1,
}

TACTIC_KILLCHAIN_DICT = {
    "TA0043": "killchain_01",
    "TA0042": "killchain_02",
    "TA0001": "killchain_03",
    "TA0002": "killchain_04",
    "TA0003": "killchain_05",
    "TA0004": "killchain_05",
    "TA0005": "killchain_05",
    "TA0006": "killchain_06",
    "TA0007": "killchain_06",
    "TA0008": "killchain_06",
    "TA0009": "killchain_06",
    "TA0010": "killchain_06",
    "TA0011": "killchain_07",
    "TA0040": "killchain_07",
}

COLUMN_MAPPING_MITIGATION = {
    "ID": "mitigation_id",
    "STIX ID": "mitigation",
    "name": "description_en",
    "description": "description_jp",
    "url": "url",
    "created": "created",
    "last modified": "last_modified",
    "domain": "domain",
    "version": "version"
}

def create_mitigation_as_records(mitigation_ecxel_path: str) -> list[Record]:
    mitigation_df = pl.read_excel(mitigation_ecxel_path)
    mitigation_df = mitigation_df.select(list(COLUMN_MAPPING_MITIGATION.keys())).rename(COLUMN_MAPPING_MITIGATION)
    mitigation_df = mitigation_df.with_columns(pl.Series("description_jp", [None]* len(mitigation_df)))
    mitigation_df = mitigation_df.with_columns([pl.col("created").str.strptime(pl.Date, "%d %B %Y"), pl.col("last_modified").str.strptime(pl.Date, "%d %B %Y")])
    return mitigation_df.to_dicts()

def create_technique_mitigation_relation_as_records(relation_ecxel_path: str) -> list[Record]:
    map_replace_map = {"source ID": "mitigation_id", "target ID": 'technique_id'}
    relation_df = pl.read_excel(relation_ecxel_path)
    relation_df = relation_df.filter(pl.col("source ID").str.starts_with("M"))
    relation_df = relation_df.select(list(map_replace_map.keys())).rename(relation_ecxel_path)
    relation_df.with_columns((pl.arange(1, relation_df.height + 1)).alias("id"))
    return relation_df.to_dicts()
     



def create_tactic_as_records(tactic_ecxel_path: str) -> list[Record]:

    df = pl.read_excel(tactic_ecxel_path)
    df = df.with_columns(pl.Series("description_jp", [None]* len(df)))
    df = df.with_columns(pl.col("ID").apply(lambda x: TACTIC_ORDER_DICT[x]).alias("sequence")).sort("sequence")
    df = df.with_columns(pl.col("ID").apply(lambda x: TACTIC_KILLCHAIN_DICT[x]).alias("killchain_id"))
    df = df.rename(COLUMN_MAPPING_TACTICS)
    return df.to_dicts()

def create_technique_as_records(ecxel_path: str) -> list[Record]:
    df = pl.read_excel(ecxel_path)
    df = df.select(list(COLUMN_MAPPING_TECHNIQUE.keys())).rename(COLUMN_MAPPING_TECHNIQUE)
    df = df.with_columns(pl.Series("description_jp", [None]* len(df)))
    return df.to_dicts()

def create_teqnique_tactic_relation_records(tactic_excel_path: str, technique_excel_path: str) -> list[Record]:
    tequnique_df = pl.read_excel(tactic_excel_path)
    tequnique_df = tequnique_df.rename(COLUMN_MAPPING_TECHNIQUE)
    tequnique_df = tequnique_df.with_columns(pl.col("tactics").str.split(",")).explode("tactics").rename({"tactics":"tactic"})
    tequnique_df = tequnique_df.with_columns(pl.col("tactic").str.strip_chars(" ")).select(["tactic", "technique_id"])

    rename = {"ID": "tactic_id","name": "tactic"}
    tactic_df = pl.read_excel(technique_excel_path)
    tactic_df = tactic_df.select(["ID", "name"]).rename(rename)

    df = tequnique_df.join(tactic_df, on = "tactic").select(["technique_id", "tactic_id"])
    df = df.with_row_count("id")
    df = df.with_columns((pl.col("id") + 1).alias("id"))

    return df.to_dicts()

def create_data_collectionlayer_relation_records(datasource_excel_file):
    # "/home/work/data/enterprise-attack-v15.1-datasources.xlsx"
    df = pl.read_excel(datasource_excel_file)
    df = df.rename(COLUMN_MAPPING_DATASOURCE).drop_nulls("collection layers")
    df = df.with_columns(pl.col("collection layers").str.split(",")).explode("collection layers").rename({"collection layers":"collection_layer"})
    df = df.with_columns(pl.col("collection_layer").str.strip_chars(" ")).select(["datasource_id", "collection_layer"])
    df = df.with_row_count("id")
    df = df.with_columns((pl.col("id") + 1).alias("id"))
    return df.to_dicts()

def create_teqnique_datasource_relation_records(technique_excel_path: str, datasource_excel_path: str) -> list[Record]:    
    tequnique_df = pl.read_excel(technique_excel_path)
    rename1 = {"ID": "technique_id","data sources": "datasources"}
    tequnique_df = tequnique_df.rename(rename1)
    tequnique_df = tequnique_df.with_columns(pl.col("datasources").str.split(",")).explode("datasources").rename({"datasources":"datasource"})
    tequnique_df = tequnique_df.with_columns(pl.col("datasource").str.strip_chars(" ")).select(["datasource", "technique_id"])
    
    
    rename = {"ID": "datasource_id","name": "datasource"}
    dataset_df = pl.read_excel(datasource_excel_path)
    dataset_df = dataset_df.rename(rename).select(["datasource_id", "datasource"])

    df = tequnique_df.join(dataset_df, on = "datasource").select(["technique_id", "datasource_id"])
    df = df.with_row_count("id")
    df = df.with_columns((pl.col("id") + 1).alias("id"))

    return df.to_dicts()

def create_collection_layer_records(datasource_excel_path: str) -> list[Record]:
    df = pl.read_excel(datasource_excel_path)
    df = df.with_columns(pl.col("collection layers").str.split(",")).explode("collection layers").rename({"collection layers":"collection layer"})
    df = df.with_columns(pl.col("collection layer").str.strip_chars(" "))
    layers = df.get_column("collection layer").unique().drop_nulls().sort().to_list()
    layer_ids = [f"CL{str(i+1).zfill(4)}" for i in range(len(layers))]
    data = [
        {"layer_id": layer_id, "collectionlayer": layer, "description_en": "", "description_jp": ""}  for layer_id,layer in zip(layer_ids,layers)
    ]
    return data


def create_addditonal_datasource_as_records():
    pass
    # datasource_ids = [datasource.datasource_id for datasource in  Datasources.select(Datasources.datasource_id)]
    # data = [{"datasource_id": datasource_id, "is_target": 0} for datasource_id in datasource_ids]
    # target_model.insert_many(data).execute()

def load_datasource_as_records(datasource_ecxel_path: str) -> list[Record]:
    dataset_df = pl.read_excel(datasource_ecxel_path)
    dataset_df = dataset_df.rename(COLUMN_MAPPING_DATASOURCE).select(list(COLUMN_MAPPING_DATASOURCE.values()))
    dataset_df = dataset_df.with_columns(pl.Series("description_jp", [None]* len(dataset_df)))

    return dataset_df.to_dicts()


def create_tactic_order():
    return [
        {"order": 3, "tactic_id": "TA0001"},
        {"order": 4, "tactic_id": "TA0002"},
        {"order": 5, "tactic_id": "TA0003"},
        {"order": 6, "tactic_id": "TA0004"},
        {"order": 7, "tactic_id": "TA0005"},
        {"order": 8, "tactic_id": "TA0006"},
        {"order": 9, "tactic_id": "TA0007"},
        {"order": 10, "tactic_id": "TA0008"},
        {"order": 11, "tactic_id": "TA0009"},
        {"order": 12, "tactic_id": "TA0010"},
        {"order": 13, "tactic_id": "TA0011"},
        {"order": 14, "tactic_id": "TA0040"},
        {"order": 2, "tactic_id": "TA0042"},
        {"order": 1, "tactic_id": "TA0043"},
    ]

def create_datasource_technique_relation(relation_path: str, datasource_path: str):
    COLUMN_MAPPING_MITIGATION = {
        "target ID": "technique_id",
        "ID": "datasource_id",
        "mapping description": "detection_en",
    }
    relation_df = pl.read_excel(relation_path)
    relation_df = relation_df.filter(pl.col("mapping type")=="detects")
    datasource_df = pl.read_excel(datasource_path)
    datasource_df = datasource_df.with_columns(pl.col("name_sub").str.strip_chars())

    df = relation_df.join(datasource_df, how="left", left_on= "source name", right_on="name_sub")
    df = df.select(list(COLUMN_MAPPING_MITIGATION.keys())).rename(COLUMN_MAPPING_MITIGATION)
    df = df.with_columns(pl.Series("detection_jp", [None]* len(df))).sort(by=["technique_id", "datasource_id"])
    return df.to_dicts()



def create_cyberkill_chain_data() -> list[Record]:
    killchain_stages_with_order = [
        {
            "killchain_id": "killchain_01",
            "phase": "Reconnaissance",
            "description_en": "Intruder selects target, researches it, and attempts to identify vulnerabilities in the target network.",
            "description_jp": "侵入者はターゲットを選択し、調査し、ターゲットネットワークの脆弱性を特定しようとします。",
            "order": 1
        },
        {
            "killchain_id": "killchain_02",
            "phase": "Weaponization",
            "description_en": "Intruder creates remote access malware weapon, such as a virus or worm, tailored to one or more vulnerabilities.",
            "description_jp": "侵入者は、ウイルスやワームなどのリモートアクセスマルウェアを作成し、1つ以上の脆弱性に合わせます。",
            "order": 2
        },
        {
            "killchain_id": "killchain_03",
            "phase": "Delivery",
            "description_en": "Intruder transmits weapon to target (e.g., via e-mail attachments, websites or USB drives).",
            "description_jp": "侵入者は、武器をターゲットに送信します（例：電子メールの添付ファイル、ウェブサイト、USBドライブなど）。",
            "order": 3
        },
        {
            "killchain_id": "killchain_04",
            "phase": "Exploitation",
            "description_en": "Malware weapon's program code triggers, which takes action on target network to exploit vulnerability.",
            "description_jp": "マルウェアのプログラムコードがトリガーされ、ターゲットネットワーク上で脆弱性を悪用するためのアクションを実行します。",
            "order": 4
        },
        {
            "killchain_id": "killchain_05",
            "phase": "Installation",
            "description_en": "Malware weapon installs an access point (e.g., 'backdoor') usable by the intruder.",
            "description_jp": "マルウェアが侵入者が使用できるアクセスポイント（例：「バックドア」）をインストールします。",
            "order": 5
        },
        {
            "killchain_id": "killchain_06",
            "phase": "Command and Control",
            "description_en": "Malware enables intruder to have 'hands on the keyboard' persistent access to the target network.",
            "description_jp": "マルウェアが侵入者に「キーボード操作」でターゲットネットワークへの持続的なアクセスを可能にします。",
            "order": 6
        },
        {
            "killchain_id": "killchain_07",
            "phase": "Actions on Objective",
            "description_en": "Intruder takes action to achieve their goals, such as data exfiltration, data destruction, or encryption for ransom.",
            "description_jp": "侵入者は、データの引き出し、データの破壊、または身代金のための暗号化などの目的を達成するために行動を起こします。",
            "order": 7
        }
    ]
    return killchain_stages_with_order



def load_tactic_as_records(ecxel_path: str) -> list[Record]:

    df = pl.read_excel(ecxel_path)
    df = df.with_columns(pl.Series("description_jp", [None]* len(df)))
    df = df.rename(COLUMN_MAPPING_TACTICS)
    return df.to_dicts()


    
def save_to_mysql(table: Model, records: list[Record]) -> None:
    table.insert_many(records).execute()


# if __name__ == "__main__":
    