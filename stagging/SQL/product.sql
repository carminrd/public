DROP VIEW IF EXISTS vw_product_master;

CREATE VIEW vw_product_master AS

with
-- master A
prod_A as (
    select 
    'AAA' || SUBSTR('00000' || CAST("商品コード" AS STRING), -5) -- 0埋め5桁　LPADかto_charある環境ならそっち使う
     as prod_cd,
    "商品カテゴリ" as category,
    "商品名" as prod_nm,
    "単価" as unit_price
    from データ統合デモ_商品マスタA
),

-- master B
prod_B_row as (
    select 
    "商品コード" as prod_cd,
    'BBB' as category,
    "商品名" as prod_nm,
    "単価" as unit_price,
    "更新日" as data_update
    from データ統合デモ_商品マスタB
    where unit_price not GLOB '*[^0-9]*'
),
prod_B_base as (
    select
    prod_cd,category,prod_nm
    from prod_B_row
    group by prod_cd,category,prod_nm
),
prod_B_curr as (
    select *
    from (
        select prod_cd,data_update,unit_price,
            ROW_NUMBER() OVER (
                PARTITION BY prod_cd 
                ORDER BY data_update DESC
            ) AS rn
        from prod_B_row
    ) t
    where rn=1
),
prod_B as (
    select a.*,b.unit_price
    from prod_B_base as a
    inner join prod_B_curr as b
    on a.prod_cd=b.prod_cd
),


-- master C
prod_C as (
    select
    product_code as prod_cd,
    SUBSTR(
        "product_group",
        INSTR("product_group", '【') + 1,
        INSTR("product_group", '】') - INSTR("product_group", '【') - 1
    ) as category,
    SUBSTR("product_group", 1, INSTR("product_group",'【') - 1) as prod_nm,
    CAST(
        CAST(unit_price AS REAL) * CAST(rate AS REAL) + 0.9999 AS INT
        ) AS unit_price
    from データ統合デモ_商品マスタC
)

select *
from prod_A

UNION ALL
select *
from prod_B

UNION ALL
select *
from prod_C
;

select *
from vw_product_master
;