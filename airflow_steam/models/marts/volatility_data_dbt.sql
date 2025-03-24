{{ config(materialized='table') }}


WITH dados_filtrados AS (
    SELECT 
        item,
        date_month,  -- Supondo que seja um formato YYYY-MM (ex: '2024-01')
        var_price::NUMERIC,  -- Garante que está como número
        TO_DATE(date_month || '-01', 'YYYY-MM-DD') AS data_formatada
    FROM agg_data_dbt
)

SELECT 

    item,
	

    ROUND(STDDEV(var_price) FILTER (WHERE data_formatada >= CURRENT_DATE - INTERVAL '3 months'),2) AS volatility_3m,
	

    ROUND(STDDEV(var_price) FILTER (WHERE data_formatada >= CURRENT_DATE - INTERVAL '6 months'),2) AS volatility_6m,
    

    ROUND(STDDEV(var_price) FILTER (WHERE data_formatada >= CURRENT_DATE - INTERVAL '12 months'),2) AS volatility_12m,
    

    ROUND(STDDEV(var_price) FILTER (WHERE data_formatada >= CURRENT_DATE - INTERVAL '24 months'),2) AS volatility_24m

FROM dados_filtrados
GROUP BY item