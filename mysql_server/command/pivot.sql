SELECT
    ds.datasource,
    t.technique,
    COUNT(*) AS combination_count
FROM
    techdata td
LEFT JOIN 
    datasources ds ON ds.datasource_id = td.datasource_id
LEFT JOIN 
    techniques t ON t.technique_id = td.technique_id
GROUP BY
    td.datasource_id,
    td.technique_id
ORDER BY
    td.datasource_id, 
    td.technique_id;
