DROP VIEW IF EXISTS vw_customers_curr;

CREATE VIEW vw_customers_curr AS

with
-- customers_AS
cst_as as(
    select
    "得意先コード" as cust_cd,
    "得意先名称" as cust_nm,
    "更新日" as updated_dt,
    "国" as country
    from データ統合デモ_得意先マスタAS
),
cst_as_base as (
    select cust_cd,cust_nm,country
    from cst_as
    group by cust_cd,cust_nm,country
),
cst_as_curr as (
    select *
    from (
        select cust_cd,updated_dt,
        ROW_NUMBER() OVER (
                PARTITION BY cust_cd 
                ORDER BY updated_dt DESC
            ) AS rn
        from cst_as
    ) t
    where rn=1
),
customers_AS as (
    select
        a.*,
        b.updated_dt,
        'AS' as area
    from cst_as_base as a
    left join cst_as_curr as b
    on a.cust_cd=b.cust_cd
),


-- customers_EU
customers_EU as(
    select
    "得意先コード" as cust_cd,
    "得意先名称" as cust_nm,
    "国" as country,
    "更新日" as updated_dt,
    'EU' as area
    from データ統合デモ_得意先マスタEU
),

-- customers_NA
customers_NA as(
    select 
    customer_code as cust_cd,
    customer_name as cust_nm,
    country,
    null as updated_dt,
    case country
        when 'USA' then 'NA'
        else 'SA'
    end as area
    from データ統合デモ_得意先マスタNA
)


select *
from customers_AS

UNION ALL
select *
from customers_EU 

UNION ALL
select *
from customers_NA
;

select *
from vw_customers_curr
;