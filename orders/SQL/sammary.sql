with T_orders_y as (
    select A.*,
    strftime('%Y-%m', order_date) AS month,
    B.customer_name,
    B.region,
    C.category,
    C.unit_price,
    quantity*unit_price as amount
    FROM T_orders as A

    left join M_customers as B
    on A.customer_id=B.customer_id

    left join M_prod as C
    on A.product_id=C.product_id
)


SELECT 
month,region,category,
count(customer_id) as odr_count,
sum(amount) as total_amount

from T_orders_y

GROUP by month,region,category

-- limit 10

;