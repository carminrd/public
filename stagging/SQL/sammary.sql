select
strftime('%Y-%m', REPLACE(order_date, '/', '-')) AS month,
b.area,
C.category,
count(order_no) as odr_count,
quantity*unit_price as amount

from vw_orders as a

inner join vw_customers_curr as b
on a.cust_cd=b.cust_cd

inner join vw_product_master as c
on a.prod_cd=c.prod_cd


GROUP by area,category
;