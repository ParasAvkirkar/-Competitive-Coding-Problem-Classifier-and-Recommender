__author__ = 'Pranay'
import sys, csv
sys.path.append("../DataBase")
import sqlDB

remaining_users = sqlDB.get_users('codeforces_user')

for user in remaining_users:
    probs = sqlDB.get_prob_codes('codeforces_prob_user_map', user)

    diff_dict_user = {'total':0, 'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0, 'J':0, 'K':0, 'L':0
                      , 'M':0, 'N':0, 'O':0, 'P':0, 'R':0, 'unknown':0}
    diff_dict_user['total'] = len(probs)
    for prob in probs:
        prob = prob[prob.index('/')+1:][0]
        try:
            diff_dict_user[prob] += 1
        except Exception as e:
            # print prob
            diff_dict_user['unknown'] += 1
    for key in diff_dict_user:
        diff_dict_user[key] = str(diff_dict_user[key])
    print 'done '+user
    sqlDB.insert_user_db('codeforces_user', user, diff_dict_user)

