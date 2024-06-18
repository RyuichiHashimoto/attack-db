SELECT 
    d.datasource_id,
    d.datasource,
    -- d.stix_id,
    -- d.description_en,
    -- d.description_jp,
    -- d.created,
    -- d.last_modified,
    -- d.version,
    d.type,
    a.is_target
    -- d.url,
    
FROM 
    datasources d
LEFT JOIN 
    additionaldatasources a
ON 
    d.datasource_id = a.datasource_id;