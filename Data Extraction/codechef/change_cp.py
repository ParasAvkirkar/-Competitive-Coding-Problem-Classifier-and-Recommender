import pickle
current_progress = {'section':0, 'problem_no':0}


# current_progress['section'] = 3

# with open('current_progress.pickle', 'w+b') as f:
# 	pickle.dump(current_progress, f)	

with open('current_progress.pickle') as f:
	current_progress = pickle.load(f)
	print current_progress['section'] , " " , current_progress['problem_no']