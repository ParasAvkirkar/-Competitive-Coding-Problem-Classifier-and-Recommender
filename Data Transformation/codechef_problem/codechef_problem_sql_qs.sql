--set codechef_problem category from our identified tags
update codechef_problem t1
join (select prob_code, codechef_tags.tag from codechef_problem, codechef_tags where codechef_problem.tag like concat('%',  codechef_tags.tag, '%')) t2 on t1.prob_code = t2.prob_code
set category = t2.tag

--match prob_code with our identified tags
select prob_code, codechef_tags.tag 
from codechef_problem, codechef_tags 
where codechef_problem.tag like concat('%',  codechef_tags.tag, '%')

--set all dp related to tag dp
UPDATE codechef_problem 
set category = 'dp' 
where category = 'dynamic-prog' or category = 'dp+bitmask'

--set all math related to tag maths
update codechef_problem
set category = 'maths'
where category = 'math' or category = 'simple-math'

--set all graphs related to tag graph
update codechef_problem
set category = 'graph'
where category = 'graphs'

--remove garbage prob statement
update codechef_problem
set description = substr(description, 48)
where description like '%All submissions for this problem are available. %'

--remove garbage prob statement
update codechef_problem
set description = substr(description, 70)
where description like '%Read problems statements in Mandarin Chinese , Russian and Vietnamese %'

update codechef_problem
set description = substr(description, 58)
where description like '%Read problems statements in Mandarin Chinese and Russian. %'

update codechef_problem
set description = substr(description, 41)
where description like '%Read problems statements in Russian here %'

update codechef_problem
set description = substr(description, 74)
where description like '%Read problems statements in English, Mandarin Chinese and Russian as well.%'

update codechef_problem
set description = substr(description, 66)
where description like '%Read problems statements in Mandarin Chinese and Russian as well. %'

update codechef_problem
set description = substr(description, 78)
where description like '%Read problems statements in Mandarin Chinese, Russian and Vietnamese as well. %'