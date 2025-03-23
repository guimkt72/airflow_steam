
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='view') }}

SELECT

    item,
    date(date) as "date",
    offers,
    round(CAST(price AS numeric), 2) as price



FROM {{ source('raw_data_source', 'raw_data_new') }}

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
