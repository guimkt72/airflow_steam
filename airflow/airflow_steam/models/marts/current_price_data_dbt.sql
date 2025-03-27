{{ config(materialized='table') }}


with tratamento1 as (
	
	select 
	price.item,
	price.price_steam,
	price.price_real,
	price.price_buff,
	last.last_price as last_price_steam
	
	from {{ ref('price_data_dbt') }} as price
	left join {{ ref('last_price_data_dbt') }} as last on last.item = price.item
),

tratamento2 as (

	select
	item,
	price_steam,
	price_real,
	price_buff,
	last_price_steam,
	round((last_price_steam * (1-0.30)),2) as last_real,
	round(((last_price_steam * (1-0.30)) / 0.80),2) as last_buff
	
	from
		tratamento1
)

	select
	*,
	
	round(((((last_price_steam - price_steam) / price_steam)) * 100),2) as var_steam,
	round(((((last_real - price_real) / price_real)) * 100),2) as var_real,
	round(((((last_buff - price_buff) / price_buff)) * 100),2) as var_buff
	
	
	from 
	tratamento2