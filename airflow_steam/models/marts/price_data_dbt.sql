{{ config(materialized='table') }}



with tratamento1 as (
	
	SELECT 
		
		item,
		date_trunc('month', date_buy) as date_buy
	
	FROM
		{{ ref('raw_data_date_buy_dbt') }}

), 
	tratamento2 as (

	SELECT
	
	buy.item,
	date(buy.date_buy) date_buy,
	agg.date_month,
	agg.med_price as price_steam,
	round((agg.med_price * (1-0.30)),2) as price_real,
	round(((agg.med_price * (1-0.30)) / 0.80),2) as price_buff
	
	
	FROM
		tratamento1 as buy
		
	LEFT JOIN 
		{{ ref('agg_data_dbt') }} as agg on agg.item = buy.item and buy.date_buy = agg.date_month
)

	SELECT 
	
	item,
	date_buy,
	price_steam,
	price_real,
	price_buff
	
	FROM
		tratamento2
		
	WHERE
	date_month is not null 
	or price_steam is not null 
	or price_real is not null 
	or price_buff is not null