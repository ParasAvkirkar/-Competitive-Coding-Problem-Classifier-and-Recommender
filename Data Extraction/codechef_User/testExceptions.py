# with open('focus.txt', 'w') as f1:
# 	with open('exceptScenarios.log', 'r') as f:
# 		for line in f:
# 			if 'User:' in line and 'Caused' in line and 'Unable' not in line:
# 				f1.write(line)
# 			elif 'User:' in line and 'refused' in line:
# 				f1.write(line)



with open('focus.txt', 'r') as f1:
	with open('users_ids.txt', 'w') as f:
		for line in f1:
			if 'asci' in line:
				try:
					uname = line[line.index('User: ') + 6: line.index('Caused') - 1]
					f.write(uname + '\n')
				except Exception as e:
					print(e)
