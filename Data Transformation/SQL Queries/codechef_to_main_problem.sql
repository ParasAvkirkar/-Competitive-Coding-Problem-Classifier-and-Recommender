INSERT INTO `Problem`(`prob_code`, `url`, `description`, 
	`modified_description`, `tags`, `category`, `time_limit`, `memory_limit`, 
	`difficulty`, `sub_size`) 

SELECT prob_code, url, description, modified_description, 
		tag, category, time_limit, source_limit, difficulty, submission_size
	from `data stage fyp`.codechef_problem

	update problem set platform = 'codechef'
where platform = ''