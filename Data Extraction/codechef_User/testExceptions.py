from collections import defaultdict

# with open('focus.txt', 'w') as f1:
# 	with open('exceptScenarios.log', 'r') as f:
# 		for line in f:
# 			if 'User:' in line and 'Caused' in line and 'Unable' not in line:
# 				f1.write(line)
# 			elif 'User:' in line and 'refused' in line:
# 				f1.write(line)



# with open('focus.txt', 'r') as f1:
# 	with open('users_ids.txt', 'w') as f:
# 		for line in f1:
# 			if 'asci' in line:
# 				try:
# 					uname = line[line.index('User: ') + 6: line.index('Caused') - 1]
# 					f.write(uname + '\n')
# 				except Exception as e:
# 					print(e)


userList = defaultdict(int)
count = 0
with open('users_ids.txt', 'r') as f:
	for line in f:
		line = line.split('\n')[0]
		userList[line] += 1

	repeatedElements = 0
	for key in userList:
		if userList[key] > 1:
			repeatedElements += 1
			#print key

	print('Repeated Elements: {0}'.format(str(repeatedElements)))
	
with open('users_ids.txt', 'r') as f:
	for line in f:
		#print 'got inside'
		count += 1
		line = line.split('\n')[0]
		if userList[line] > 1:
			print('Id repeated: {0}'.format(line))
			print(str(count))
		if count > 100:
			break

