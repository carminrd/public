DROP VIEW IF EXISTS vw_orders;

CREATE VIEW vw_orders AS

with odr as(
    select
    "オーダーID" as order_no,
    "オーダーID枝番" as order_seq,
    "受付日" as order_date,
    "得意先コード" as cust_cd,
    "商品コード" as prod_cd,
    "ステータス" as status,
    "数量" as quantity
    from データ統合デモ_オーダー
),
fst_odr as(
    select 
    order_no,
    order_date,
    cust_cd,
    prod_cd,
    quantity
    from odr
    where order_seq=1
), 
current_odr as(
    SELECT *
    FROM (
        SELECT
            order_no,
            status,
            order_date,
            ROW_NUMBER() OVER (
                PARTITION BY order_no
                ORDER BY order_date DESC
            ) AS rn
        FROM odr
    ) as t
    WHERE rn = 1
)

SELECT
    a.order_no,
    a.order_date,
    a.cust_cd,
    a.prod_cd,
    a.quantity,
    b.status AS curr_status,
    b.order_date as status_date
FROM fst_odr AS a

inner join current_odr as b
on a.order_no=b.order_no

;

select *
from vw_orders
;