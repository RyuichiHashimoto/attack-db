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

def load_tactic_as_records(ecxel_path: str) -> list[Record]:

    df = pl.read_excel(ecxel_path)
    df = df.with_columns(pl.Series("description_jp", [None]* len(df)))
    df = df.rename(COLUMN_MAPPING_TACTICS)
    return df.to_dicts()

def load_teqnique_as_records(ecxel_path: str) -> list[Record]:
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


def load_tactic_as_records(ecxel_path: str) -> list[Record]:

    df = pl.read_excel(ecxel_path)
    df = df.with_columns(pl.Series("description_jp", [None]* len(df)))
    df = df.rename(COLUMN_MAPPING_TACTICS)
    return df.to_dicts()


    
def save_to_mysql(table: Model, records: list[Record]) -> None:
    table.insert_many(records).execute()


# if __name__ == "__main__":
    