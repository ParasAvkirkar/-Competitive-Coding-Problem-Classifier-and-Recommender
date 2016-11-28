from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from itertools import groupby

from codeforcesuser import CodeForcesUser, UserSubmission
import requests
import json
import pickle
import os
import time, sys
sys.path.append("../DataBase")
import sqlDB


def fetch_user(userLink, driver):
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

		submissionsList = fetch_submissions(resultList)

		for problem in resultList:
			if 'ok' in  problem['verdict'].lower():
				problemDict = problem
				problemDetailDict = problemDict['problem']
				# print problemDetailDict['contestId']
				# print problemDetailDict['index']
				problemCodes.append(str(problemDetailDict['contestId']) + '/' + str(problemDetailDict['index']))

		submission_link = 'http://codeforces.com/submissions/'+stringUserDict.get('handle', '')
		driver.get(submission_link)
		table = driver.find_element_by_class_name('status-frame-datatable')
		rows = table.find_elements(By.TAG_NAME, 'tr')
		langs = {}
		for row in rows[1:]:
			cols = row.find_elements(By.TAG_NAME, 'td')
			if cols[4].text in langs:
				langs[cols[4].text] += 1
			else:
				langs[cols[4].text] = 1
		prefLang = ""
		max = -1;
		for key in langs:
			if langs[key] > max:
				prefLang = key
				max = langs[key]

		user = CodeForcesUser(codeforcesProfileUrl + stringUserDict.get('handle', ''), stringUserDict.get('handle', ''),
								stringUserDict.get('firstName', '') + ' ' + stringUserDict.get('lastName', ''), 
								stringUserDict.get('country', ''), stringUserDict.get('city', ''), stringUserDict.get('organization', ''),
								problemCodes, submissionsList, stringUserDict.get('rating', ''), stringUserDict.get('rank', ''), prefLang)

	
	except Exception as e:
		print(e)
		user = None
	finally:
		return user

def fetch_submissions(resultList):
	
	try:
		sortedList = sorted(resultList, key=lambda d: (d['problem']['contestId'], d['problem']['index']))
		groups = groupby(sortedList, key=lambda d: (d['problem']['contestId'], d['problem']['index']))
		submissionCountList = [(k, len(list(g))) for k, g in groups]
		
		successfulSubmissionCountDict = {}
		for t in submissionCountList:
			successfulSubmissionCountDict[str(t[0][0]) + "/" + str(t[0][1])] = str(t[1])

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
		print submissionsList
	except Exception as e:
		print(e)
		submissionsList = Error
	finally:
		return submissionsList

if __name__ == '__main__':
	driver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
	with open('texts/supuserList.txt') as listF:
		userHandles = listF.read().splitlines()
		count = 0
		print('till here')
		if os.path.exists('curr_progress'):
			with open('curr_progress', 'rb') as progRead:
				count = pickle.load(progRead)

		#print(userHandles)
		for i in range(count, 1000):
			with open('curr_progress', 'wb') as progWrite:
				pickle.dump(count, progWrite)
				count = count + 1

			user = fetch_user('http://codeforces.com/api/user.info?handles='+ userHandles[i] +';', driver)
			if user:
				sqlDB.insert_user_db('codeforces_user', user.uname, user.country, user.city, True, user.submissions, user.pref_lang, user.ratings, user.rank)
			# with open('users/' + userHandles[i], 'wb') as userWrite:
			# 	pickle.dump(user, userWrite)
			print('count = ' + str(count) + ' ' + str(user))