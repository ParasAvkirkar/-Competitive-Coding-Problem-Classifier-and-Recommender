from selenium import webdriver
from bs4 import BeautifulSoup

from itertools import groupby

from codeforcesuser import CodeForcesUser, UserSubmission
import requests
import json
import pickle
import os
import sys
import logging
import datetime
import time, sys
import operator

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../DataBase")
import sqlDB

sys.path.append("../Utilities")
#from driverUtil import getDriver

#1400 - 2300 users not scraped net failure

def fetch_user(userLink):
	try:

		codeforcesProfileUrl = 'http://codeforces.com/profile/'
		# baseUrl = "http://www.spoj.com/users/"
		# userLink = baseUrl + uname
		# driver.get(userLink)
		response = requests.get(userLink)

		jsonResponse = json.loads(response.content)
		resultList = jsonResponse['result']
		userDict = resultList[0]
		stringUserDict = {}
		for key in userDict:
			stringUserDict[key] = str(userDict[key])
			# print key
			# print userDict[key]
		#response = requests.get('http://codeforces.com/api/user.status?handle='+ userDict['handle']+'&from=1&count=10000')
		response = requests.get('http://codeforces.com/api/user.status?handle='+ userDict['handle'])
		jsonResponse = json.loads(response.content)
		resultList = jsonResponse['result']

		problemCodes = []
		submissionsList, prefLang = fetch_submissions(resultList, userDict['handle'])
		for problem in resultList:
			if 'ok' in  problem['verdict'].lower():
				problemDict = problem
				problemDetailDict = problemDict['problem']
				# print problemDetailDict['contestId']
				# print problemDetailDict['index']
				problemCodes.append(str(problemDetailDict['contestId']) + '/' + str(problemDetailDict['index']))
		
		user = CodeForcesUser(codeforcesProfileUrl + stringUserDict.get('handle', ''), stringUserDict.get('handle', ''),
								stringUserDict.get('firstName', '') + ' ' + stringUserDict.get('lastName', ''), 
								stringUserDict.get('country', ''), stringUserDict.get('city', ''), stringUserDict.get('organization', ''),
								problemCodes, submissionsList, stringUserDict.get('rating', ''), stringUserDict.get('rank', ''), prefLang)

	
	except Exception as e:
		print(e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print 'Exception at line '+ str(exc_tb.tb_lineno)
		logging.error('Time: {0} File: {1} Line: {2} UserURL: {3} Caused By: {4}'.format(datetime.datetime.now(), os.path.basename(__file__),
								exc_tb.tb_lineno, userLink, e))
		# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
		# 		' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))
		user = None
	finally:
		return user

def fetch_submissions(resultList, handle):
	
	try:
		sortedList = sorted(resultList, key=lambda d: (d['problem']['contestId'], d['problem']['index']))
		groups = groupby(sortedList, key=lambda d: (d['problem']['contestId'], d['problem']['index']))
		submissionCountList = [(k, len(list(g))) for k, g in groups]
		
		successfulSubmissionCountDict = {}
		for t in submissionCountList:
			successfulSubmissionCountDict[str(t[0][0]) + "/" + str(t[0][1])] = str(t[1])

		sortedList = sorted(resultList, key=lambda d: (d['programmingLanguage']))
		groups = groupby(sortedList, key=lambda d: (d['programmingLanguage']))
		languagesList = [(k, len(list(g))) for k, g in groups]
		
		languageCountDict = {}
		stdLanguageCountDict = {}

		for t in languagesList:
			languageCountDict[str(t[0])] = t[1]
		
		with open('texts/languages.txt') as listF:
			langList = listF.read().splitlines()
		
		for lang in languageCountDict:
			for stdlang in langList:
				if  stdlang.lower() in lang.lower():
					try:
						stdLanguageCountDict[stdlang] += languageCountDict[lang]
					except:
						stdLanguageCountDict[stdlang] = languageCountDict[lang]
					break
		
		prefferedLanguage = max(stdLanguageCountDict.iteritems(), key=operator.itemgetter(1))[0]
		
		result = [t for t in resultList if 'ok' in  t['verdict'].lower()]
		sortedList = sorted(result, key=lambda d: (d['problem']['contestId'], d['problem']['index']))
		groups = groupby(sortedList, key=lambda d: (d['problem']['contestId'], d['problem']['index']))
		submissionDateList = [(k, max(g, key=lambda d: d['creationTimeSeconds'])) for k, g in groups]
		
		submissionsList = []

		for date in submissionDateList:
			problemId = str(date[0][0]) + "/" + str(date[0][1])
			submissionCount = successfulSubmissionCountDict[problemId]
			submissionDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date[1].get('creationTimeSeconds')))
			submissionDetails = UserSubmission(problemId, submissionCount, submissionDate)
			submissionsList.append(submissionDetails)
		#print submissionsList
	except Exception as e:
		submissionsList = Error
		#print(e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print 'Exception at line '+ str(exc_tb.tb_lineno)
		logging.error('Time: {0} File: {1} Line: {2} Link: {3} Caused By: {4}'.format(datetime.datetime.now(), os.path.basename(__file__),
								exc_tb.tb_lineno, str(handle), e))
		# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
		# 		' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))
	finally:
		return submissionsList, prefferedLanguage

if __name__ == '__main__':
	# driver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
	
	#driver = getDriver()
	logging.basicConfig(filename='exceptScenarios.log', level=logging.ERROR)
	try:
		with open('texts/supuserList.txt') as listF:
			userHandles = listF.read().splitlines()
			count = 0
			print('till here')
			if os.path.exists('curr_progress'):
				with open('curr_progress', 'rb') as progRead:
					count = pickle.load(progRead)
			#print(userHandles)
			for i in range(count, 20000):
				with open('curr_progress', 'wb') as progWrite:
					pickle.dump(count, progWrite)
					count = count + 1
				user = fetch_user('http://codeforces.com/api/user.info?handles='+ userHandles[i] +';')
				if user:
					sqlDB.insert_user_db('codeforces_user', user.uname, user.country, user.city, True, user.submissions, user.pref_lang, user.ratings, user.rank)
				# with open('users/' + userHandles[i], 'wb') as userWrite:
				# 	pickle.dump(user, userWrite)
				print('count = ' + str(count) + ' ' + str(user))
	except Exception as e:
		print(e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print 'Exception at line '+ str(exc_tb.tb_lineno)
		logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}'.format(datetime.datetime.now(), os.path.basename(__file__),
								exc_tb.tb_lineno, e))
		# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
		# 		' :Line Number: '+ str(exc_tb.tb_lineno) + ' :Caused By: ' + str(e))	