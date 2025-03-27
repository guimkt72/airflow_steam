
{{ config(materialized='table') }}


with tratamento1 as (
	
	select 
	
		*,
		case when 1=1 then 'Inventory' else '0' end as "inventory"
	
		from 
			{{ ref('current_price_data_dbt') }}
),

	tratamento2 as (

	select 
	
	inventory,
	sum(price_steam) as sum_price_steam,
	sum(price_real) as sum_price_real,
	sum(price_buff) as sum_price_buff,
	sum(last_price_steam) as sum_last_price_steam,
	sum(last_real) as sum_last_real,
	sum(last_buff) as sum_last_buff
	
	from
		tratamento1
	group by 
		1
	order by 
		1
)

	select
	
	*,
	round(((((sum_last_price_steam - sum_price_steam) / sum_price_steam)) * 100),2) as var_steam,
	round(((((sum_last_real - sum_price_real) / sum_price_real)) * 100),2) as var_real,
	round(((((sum_last_buff - sum_price_buff) / sum_price_buff)) * 100),2) as var_buff
		
	FROM
		tratamento2
		
	group by 1,2,3,4,5,6,7