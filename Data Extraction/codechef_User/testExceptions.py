with open('focus.txt', 'w') as f1:
	with open('exceptScenarios.log', 'r') as f:
		for line in f:
			if 'User:' in line and 'Caused' in line and 'Unable' not in line:
				f1.write(line)
			elif 'User:' in line and 'refused' in line:
				f1.write(line)