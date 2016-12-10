import MySQLdb
import sys
import os
import logging
import datetime


def connect_db():
		# Open database connection
		try:
			with open("dbINFO.txt", "r+b") as f:
				ip, username, password, db_name = f.read().split('\n')
		except Exception as e:
			ip = "localhost"
			username = "root"
			password = ""
			db_name = "data stage fyp"
			print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print 'Exception at line '+ str(exc_tb.tb_lineno)
			logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
					' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))				

		db = MySQLdb.connect(ip, username, password, db_name)
		return db

def insert_user_db(tableName, uname, country, userCity, isStudent, userSubmissions, prefLang, rating, rank):
		try:
			q = ''
			if tableName == 'codechef_user':
				q = "INSERT INTO "+ tableName +" VALUES ( " + "null, '" + uname + "', '" + country + "', '" + userCity + "', '" \
					+ str(isStudent) + "', '" + prefLang + "', '" + str(rating['Long']) + "', '" + str(rating['Short']) +"', '" + str(rating['LTime']) +"', '" + str(rank['Long']) +"', '"+ str(rank['Short']) +"', '" + str(rank['LTime']) + "');\n"
			elif tableName == 'spoj_user' or tableName == 'codeforces_user':
				q = "INSERT INTO "+ tableName +" VALUES ( " + "null, '" + uname + "', '" + country + "', '" + userCity + "', '" \
					+ str(isStudent) + "', '" + prefLang + "', '" + str(rating) + "', '" + str(rating) +"', '" + str(rating) +"', '" + str(rank) +"', '"+ str(rank) +"', '" + str(rank) + "');\n"

			db = connect_db()
			# prepare a cursor object using cursor() method
			cursor = db.cursor()

			# execute SQL query using execute() method.
			if cursor.execute(q) == 1:
				db.commit()
				# print "Success DB"
			else:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
					' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(q)) 
				# print "Fail DB"
			# print userSubmissions
			for submission in userSubmissions:
				# print (submission)
				if len(submission.problemCode)>0:
					q = "INSERT INTO "+tableName.split("_")[0]+"_prob_user_map VALUES (null, '"+uname+"', '"+submission.problemCode+"', \
						'"+str(submission.time)+"', '"+str(submission.noOfSubmissions)+"' )"
					# print q
					if cursor.execute(q) == 1:
						db.commit()
						# print "Success DB"
					else: 
						exc_type, exc_obj, exc_tb = sys.exc_info()
						logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
								' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(q)) 
						# print "Fail DB"
			db.close()
		except Exception as e:
			# print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			# print 'Exception at line '+ str(exc_tb.tb_lineno)
			logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
					' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))


def insert_problem_db(tableName, prob_code, url, desc, tag, diff, category, sub_size, constraint, time_limit, source_limit, is_example_given):
		try:
			q = "INSERT INTO "+tableName+" VALUES(NULL, '"+(prob_code)+"', '"+str(url)+"', '"+(desc)+"', '"+(tag)+"', '"+str(sub_size)+"', " \
				"'"+(constraint)+"', '"+str(is_example_given)+"', '"+str(diff)+"', '"+str(category)+"', '"+str(time_limit)+"', '"+str(source_limit)+"') ;"

			# print q

			db = connect_db()
			db.set_character_set('utf8')
			# prepare a cursor object using cursor() method
			cursor = db.cursor()
			cursor.execute('SET NAMES utf8;')
			cursor.execute('SET CHARACTER SET utf8;')
			cursor.execute('SET character_set_connection=utf8;')
			# execute SQL query using execute() method.
			if cursor.execute(q) == 1:
				db.commit()
				print "Success DB"
			else:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
					' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(q))  
				print "Fail DB"
			db.close()
		except Exception as e:
			# print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			# print 'Exception at line '+ str(exc_tb.tb_lineno)
			logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
					' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))


def does_user_exist(username, tablename):
	try:
		q = "SELECT count(uname) FROM `"+tablename+"` WHERE uname='"+ username +"'"
		db = connect_db()
		# prepare a cursor object using cursor() method
		cursor = db.cursor()
		cursor.execute(q)
		result = cursor.fetchall()
		result = result[0][0]
		db.close()
		if result==1:
			return True
		return False
	except Exception as e:
			# print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			# print 'Exception at line '+ str(exc_tb.tb_lineno)
			logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
					' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))
