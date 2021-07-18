--TODO: this needs to be rewritten once ELO rankings are implemented
select 
    coalesce(w.ytVid_id, l.ytVid_id) 
    ,coalesce(wincount, 0) / cast(appearances as float) as winRatio
--    ,coalesce(wincount, 0) as winCount
--    ,a.appearances
from (
    select 
        ytVid_id
        ,count(*) as appearances
    from bracket_bettervote 
    group by
        ytVid_id
) a
left join (
    select 
        ytVid_id
        ,outcome
        ,count(*) as wincount
    from bracket_bettervote
    where outcome = 'W'
    group by
        ytVid_id
        ,outcome
) w on a.ytVid_id = w.ytVid_id
left join (
    select 
        ytVid_id
        ,outcome
        ,count(*)  as losscount
    from bracket_bettervote
    where outcome = 'L'
    group by
        ytVid_id
        ,outcome
) l on a.ytVid_id = l.ytVid_id
order by (coalesce(wincount, 0) / cast(appearances as float)) desc, appearances desc
limit :resultLimit;