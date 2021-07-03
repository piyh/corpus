select 
    coalesce(w.ytid, l.ytid) as ytid
    ,coalesce(wincount, 0) / cast(appearances as float) as winRatio
--    ,coalesce(wincount, 0) as winCount
--    ,a.appearances
from (
    select 
        ytid
        ,count(*) as appearances
    from normalizedVotes 
    group by
        ytid
) a
left join (
    select 
        ytid
        ,outcome
        ,count(*) as wincount
    from normalizedVotes 
    where outcome = 'win'
    group by
        ytid
        ,outcome
) w on a.ytid = w.ytid
left join (
    select 
        ytid
        ,outcome
        ,count(*)  as losscount
    from normalizedVotes 
    where outcome = 'loss'
    group by
        ytid
        ,outcome
) l on a.ytid = l.ytid
order by (coalesce(wincount, 0) / cast(appearances as float)) desc, appearances desc
limit :resultLimit;