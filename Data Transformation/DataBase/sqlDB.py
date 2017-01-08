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
			# print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			# print 'Exception at line '+ str(exc_tb.tb_lineno)
			logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
					' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))				

		db = MySQLdb.connect(ip, username, password, db_name)
		return db

def insert_user_db(tableName, uname, difficulties):
		try:
			q = ''
			if tableName == 'codechef_user':
				q = "UPDATE `codechef_user` SET `total_solved`='"+difficulties['total']+"',`easy_solved`='"+difficulties['easy']+"',`medium_solved`='"+difficulties['medium']+"'," \
					"`hard_solved`='"+difficulties['hard']+"',`challenge_solved`='"+difficulties['challenge']+"',`school_solved`='"+difficulties['school']+"',`unknown_solved`='"+difficulties['unknown']+"' " \
					"WHERE uname = '"+uname+"'"
				# print q
			elif tableName == 'spoj_user' or tableName == 'codeforces_user':
				q = "UPDATE `codeforces_user` SET `total_solved`='"+difficulties['total']+"',`a_solved`='"+difficulties['A']+"',`b_solved`='"+difficulties['B']+"',`c_solved`='"+difficulties['C']+"',`d_solved`='"+difficulties['D']+"'," \
					"`e_solved`='"+difficulties['E']+"',`f_solved`='"+difficulties['F']+"',`g_solved`='"+difficulties['G']+"',`h_solved`='"+difficulties['H']+"',`i_solved`='"+difficulties['I']+"',`j_solved`='"+difficulties['J']+"',`k_solved`='"+difficulties['K']+"'," \
					"`l_solved`='"+difficulties['L']+"',`m_solved`='"+difficulties['M']+"',`n_solved`='"+difficulties['N']+"',`o_solved`='"+difficulties['O']+"',`p_solved`='"+difficulties['P']+"',`r_solved`='"+difficulties['R']+"',`unknown_solved`='"+difficulties['unknown']+"' " \
					"WHERE uname = '"+uname+"'"
				# print q
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
	try:
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
	except Exception as e:
		print e

def get_prob_codes(table_name, uname):
	try:
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
	except Exception as e:
		print e