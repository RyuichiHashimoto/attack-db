SELECT
    ck.phase AS killchain,
    tc.tactic AS tactic,
    t.technique AS technique,
    c.collection_layer AS collection_layer,
    ds.datasource AS datasource,
    t.url
FROM
    techniques t
    LEFT JOIN tactech tt ON t.technique_id = tt.technique_id
    LEFT JOIN tactics tc ON tt.tactic_id = tc.tactic_id
    LEFT JOIN techdata td ON t.technique_id = td.technique_id
    LEFT JOIN datasources ds ON td.datasource_id = ds.datasource_id
    LEFT JOIN datacollection c ON ds.datasource_id = c.datasource_id
    LEFT JOIN cyberkillchain ck ON tc.killchain_id = ck.killchain_id
WHERE
    "1" = "1"
    # c.collection_layer = "HOST"
    # c.collection_layer = "Network"
    AND c.collection_layer in ("HOST", "Network", "OSINT")
    -- AND tc.tactic in (
    --     "Reconnaissance",
    --     "Resource Development",
    --     "Initial Access"
    -- )
    AND tc.tactic in (
        "Initial Access",
        "Execution",
        "Persistence",
        "Privilege Escalation",
        "Defense Evasion",
        "Credential Access",
        "Discovery",
        "Lateral Movement",
        "Collection",
        "Command and Control"
    )
    # AND tc.tactic in ("Exfiltration", , "Impact")
    AND t.is_sub_technique = false
ORDER BY tc.sequence;
# INTO
#     # OUTFILE '/home/work/mysql_server/command/output1.csv'
#     OUTFILE './1_intrusion.csv'
#     FIELDS TERMINATED BY ','
#     ENCLOSED BY '"'
#     LINES TERMINATED BY '\n';