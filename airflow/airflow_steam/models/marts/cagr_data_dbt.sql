

{{ config(materialized='table') }}


with tratamento1 as (
	
	select 
	
	price.item,
	price.price_real,
	price.last_real,
	buy.date_buy
	
	from
	    {{ ref('current_price_data_dbt') }} as price
	
	left join {{ ref('raw_data_date_buy_dbt') }} as buy on buy.item = price.item		
),

	tratamento2 as (
	select 
	
	item,
	price_real,
	last_real,
    EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM date_buy) AS year_diff,
	    CASE  
        WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM date_buy) > 0  
        THEN POWER(last_real / price_real, 1.0 / (EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM date_buy))) - 1  
        ELSE NULL  
    END AS cagr 

	from
		tratamento1
)

	select
	
	item,
	price_real,
	last_real,
	year_diff,
	round((POWER(last_real / price_real, 1.0 / year_diff) - 1) * 100 ,2) AS cagr_percent
	
	from 
		tratamento2