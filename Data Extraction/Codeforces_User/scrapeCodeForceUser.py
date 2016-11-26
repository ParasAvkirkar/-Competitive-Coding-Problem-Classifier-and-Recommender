from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from itertools import groupby

from codeforcesuser import CodeForcesUser
import requests
import json
import pickle
import os
import time

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

		submissionsList = fetch_submissions(resultList)

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
								problemCodes, submissionsList, stringUserDict.get('rating', ''), stringUserDict.get('rank', ''))

	
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
			submissionDetails = {"problemId" : problemId, "submissionDate" : submissionDate, "submissionCount" : submissionCount}
			submissionsList.append(submissionDetails)

	except Exception as e:
		print(e)
		submissionsList = Error
	finally:
		return submissionsList

if __name__ == '__main__':
	#driver = webdriver.Chrome()
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

			user = fetch_user('http://codeforces.com/api/user.info?handles='+ userHandles[i] +';')
			with open('users/' + userHandles[i], 'wb') as userWrite:
				pickle.dump(user, userWrite)
			print('count = ' + str(count) + ' ' + str(user))