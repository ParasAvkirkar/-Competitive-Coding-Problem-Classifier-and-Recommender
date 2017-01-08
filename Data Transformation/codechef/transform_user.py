__author__ = 'Pranay'
import sys, csv
sys.path.append("../DataBase")
import sqlDB

diff_dict = {'easy':[], 'medium':[], 'hard':[], 'challenge':[], 'school':[]}
with open('prob_diff.csv') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		prob_code = row[0]
		diff = row[1]
		diff_dict[diff].append(prob_code)

# for i in diff_dict.keys():
#     print i
#     print diff_dict[i]

remaining_users = sqlDB.get_users('codechef_user')

for user in remaining_users:
	probs = sqlDB.get_prob_codes('codechef_prob_user_map', user)
	diff_dict_user = {'total':0, 'easy':0, 'medium':0, 'hard':0, 'challenge':0, 'school':0, 'unknown':0}
	diff_dict_user['total'] = len(probs)
	for prob in probs:
		try:
			f = 0
			for key in diff_dict:
				if prob in diff_dict[key]:
					diff_dict_user[key] += 1
					f = 1
			if f==0:
				diff_dict_user['unknown'] += 1
		except Exception as e:
			print e
	for key in diff_dict_user:
		diff_dict_user[key] = str(diff_dict_user[key])
	sqlDB.insert_user_db('codechef_user', user, diff_dict_user)
	# print user
	# print diff_dict_user









