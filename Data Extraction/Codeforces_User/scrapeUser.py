from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from codeforcesuser import CodeForcesUser
import requests
import json
import pickle
import os


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

		response = requests.get('http://codeforces.com/api/user.status?handle='+ userDict['handle']+'&from=1&count=10000')
		jsonResponse = json.loads(response.content)
		resultList = jsonResponse['result']
		problemCodes = []
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
								problemCodes, stringUserDict.get('rating', ''), stringUserDict.get('rank', ''))

	
	except Exception as e:
		print(e)
		user = None
	finally:
		return user


if __name__ == '__main__':
	#driver = webdriver.Chrome()
	with open('supuserList.txt') as listF:
		userHandles = listF.read().splitlines()
    	count = 0
    	print('till here')
    	if os.path.exists('curr_progress'):
    		with open('curr_progress', 'rb') as progRead:
    			count = pickle.loads(progRead)

    	print('got inside')
		for i in range(count, len(userHandles)):
			print 'got inside'
			with open('curr_progress', 'wb') as progWrite:
				pickle.dump(count, progWrite)
				count = count + 1

			user = fetch_user('http://codeforces.com/api/user.info?handles='+ userHandles[i] +';')
			with open('users/' + userHandles[i], 'wb') as userWrite:
				pickle.dump(user, userWrite)
			print('count = ' + str(count) + ' ' + str(user))
			


			