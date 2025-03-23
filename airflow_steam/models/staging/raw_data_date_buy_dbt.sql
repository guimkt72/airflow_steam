


{{ config(materialized='view') }}

SELECT

    item,
    date(date_buy) as "date_buy"




FROM {{ source('raw_data_source', 'raw_data_date_buy') }}