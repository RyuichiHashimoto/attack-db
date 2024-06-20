#mysqldump --ssl-mode="DISABLED" --single-transaction -h miter-attack-db  -u hashimoto -phashimoto miter-attack   > $1
mysqldump --skip-ssl --single-transaction -h miter-attack-db  -u hashimoto -phashimoto miter-attack   > $1
