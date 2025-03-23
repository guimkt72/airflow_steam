



{{ config(materialized='table') }}





SELECT

	item,
	date("date") as "day",
	offers,
	price
	
	FROM 
		{{ ref('raw_data_dbt') }}




