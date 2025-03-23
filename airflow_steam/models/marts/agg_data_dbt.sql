



{{ config(materialized='table') }}





SELECT

	item,
	date(date_trunc('month', "date")) as date_month,
	round(sum(offers),2) as med_offers,
	round(avg(price),2) as med_price,
	round(
	(avg(price) - lag(avg(price)) OVER (PARTITION BY item ORDER BY date(date_trunc('month', "date")))) 
	/ lag(avg(price)) OVER (PARTITION BY item ORDER BY date(date_trunc('month', "date"))) 
	* 100, 2) AS var_price
	
	FROM 
		{{ ref('raw_data_dbt') }}
		
	GROUP BY
		1,2
		
	ORDER BY
		2 asc 



