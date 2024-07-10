#  mysql --skip-ssl -h miter-attack-db  -proot miter-attack  --batch --silent  < mysql
# SELECT 'technique_id', 'technique_name', 'tactic_name', 'datasource_id', 'datasource', 'collection_layer', 'URL'
# UNION ALL
SELECT tc.tactic AS tactic_name, tc.order AS order

FROM techniques t