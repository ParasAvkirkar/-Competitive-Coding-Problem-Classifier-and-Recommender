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

def insert_user_db(tableName, uname, total_solved, easy_solved, medium_solved, hard_solved, challenge_solved, school_solved, unknown_solved):
		try:
			q = ''
			if tableName == 'codechef_user':
				q = "UPDATE `codechef_user` SET `total_solved`='"+total_solved+"',`easy_solved`='"+easy_solved+"',`medium_solved`='"+medium_solved+"'," \
					"`hard_solved`='"+hard_solved+"',`challenge_solved`='"+challenge_solved+"',`school_solved`='"+school_solved+"',`unknown_solved`='"+unknown_solved+"' " \
					"WHERE uname = '"+uname+"'"
				# print q
			elif tableName == 'spoj_user' or tableName == 'codeforces_user':
				q = ""
				# print tableName

			db = connect_db()
			# prepare a cursor object using cursor() method
			cursor = db.cursor()

			# execute SQL query using execute() method.
			if cursor.execute(q) == 1:
				db.commit()
				# print "Success DB"
			else:
				print 'Fail DB'
				exc_type, exc_obj, exc_tb = sys.exc_info()
				logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
					' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(q))
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print exc_tb
			pass


def get_users(table_name):
	q = "select uname from `"+table_name+"`  WHERE total_solved is null"
	db = connect_db()
	cursor = db.cursor()
	cursor.execute(q)
	result = cursor.fetchall()
	users = []
	for row in result:
		users.append(row[0])
	db.close()
	return users

def get_prob_codes(table_name, uname):
	prob_codes = []
	q = "SELECT prob_code FROM `"+ table_name +"` WHERE uname = '"+ uname +"' "
	db = connect_db()
	cursor = db.cursor()
	cursor.execute(q)
	result = cursor.fetchall()
	for row in result:
		prob_codes.append(row[0])
	db.close()
	return prob_codes