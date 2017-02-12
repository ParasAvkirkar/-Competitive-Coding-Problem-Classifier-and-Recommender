INSERT INTO `Problem`(`prob_code`, `url`, `description`, 
	`modified_description`, `tags`, `category`, `time_limit`, `memory_limit`, 
	`difficulty`) 

SELECT problemId, url, description, modified_description, 
		tags, modified_tags, timelimit, memorylimit, difficulty
	from `data stage fyp`.codeforces_problems

update problem set platform = 'codeforces', sub_size = '0'