--From the two most commonly appearing regions, which is the latest datasource?
----Answer: Prague and Turin and the two regions that have more trips, in which the latest datasource for Prague is cheap_mobile with a date of 2018-05-29 12:44:02, 
----while for Turin it is pt_search_app and it was register on 2018-05-31 06:20:59
with top_two_region as(
    select region
    from trips
    group by region
    order by count(*) desc
    limit 2
)

select distinct on (a.region) a.region, a.datasource, a.datetime
from trips a
inner join top_two_region b on a.region = b.region
order by region, datetime desc
;

--What regions has the "cheap_mobile" datasource appeared in?
----Answer: The regions that where the datasource "cheap_mobile" appeared are Hamburg, Prague, Turin
select distinct region
from trips
where datasource = 'cheap_mobile'
;