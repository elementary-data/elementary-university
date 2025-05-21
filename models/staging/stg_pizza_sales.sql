with source as (

    select * from {{ source('ecom', 'raw_pizza_sales') }}

),

renamed as (

    select

        ---------- ids
        pizza_id,
        order_id,

        ---------- text / name
        pizza_name_id,
        pizza_name,
        pizza_category,
        pizza_size,

        ---------- numeric
        quantity,
        unit_price,
        total_price,

        ---------- datetime
        order_date,
        order_time,

        ---------- ingredients
        ingredient_names,
        ingredient_ids

    from source

)

select * from renamed
