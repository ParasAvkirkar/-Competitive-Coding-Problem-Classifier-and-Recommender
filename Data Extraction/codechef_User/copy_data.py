__author__ = 'Pranay'
import csv, sys
sys.path.append("../DataBase")
import sqlDB

def insert_user_db(tableName, uname, country, userCity, isStudent, prefLang, rat_long, rat_short, rat_lt, rank_long,
				   rank_short, rank_lt):

		q = "INSERT INTO "+ tableName +" VALUES ( " + "null, '" + uname + "', '" + country + "', '" + userCity + "', '" \
				+ str(isStudent) + "', '" + prefLang + "', '" + rat_long + "', '" + rat_short +"', '" + rat_lt +\
					"', '" + rank_long +"', '"+ rank_short +"', '" + rank_lt + "', "+\
			"null, null, null, null, null, null, null"+" );\n"
		# print q
		db = sqlDB.connect_db()
		# prepare a cursor object using cursor() method
		cursor = db.cursor()

			# execute SQL query using execute() method.
		if cursor.execute(q) == 1:
			db.commit()
			print "Success DB"
		else:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			# print exc_type
			print "Fail DB"



def insert_user_map_db(tableName, uname, prob_code, date, subs):
		q = "INSERT INTO "+tableName +" VALUES (null, '"+uname+"', '"+prob_code+"', \
						'"+date+"', '"+subs+"' )"
		# print q
		db = sqlDB.connect_db()
			# prepare a cursor object using cursor() method
		cursor = db.cursor()

			# execute SQL query using execute() method.
		if cursor.execute(q) == 1:
			db.commit()
			print "Success DB"
		else:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			# print exc_type
			print "Fail DB"

entered_user = []
with open('codechef_user.csv') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		uname = row[1]
		if not sqlDB.does_user_exist(uname, 'codechef_user'):
			insert_user_db('codechef_user', uname, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
			entered_user.append(uname)


with open('codechef_map.csv') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		uname = row[1]
		if uname in entered_user:
			# print uname+'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`'
			insert_user_map_db('codechef_prob_user_map', uname, row[2], row[3], row[4])

# print entered_user
