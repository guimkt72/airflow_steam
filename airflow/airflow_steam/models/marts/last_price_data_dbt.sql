
{{ config(materialized='table') }}


	with tratamento1 as (
	
	SELECT 
	
		item,
		max(day) as last_date
	
	FROM {{ ref('daily_data_dbt') }}
	
	GROUP BY item
	
	order by 1
	)
	
	SELECT 
	
		trat.item,
		trat.last_date,
		min(daily.price) as last_price
		
		FROM 
			tratamento1 as trat
			LEFT JOIN daily_data_dbt as daily
			on trat.item = daily.item 
			and daily.day = trat.last_date
			
		GROUP BY 1,2
		order by 1,2