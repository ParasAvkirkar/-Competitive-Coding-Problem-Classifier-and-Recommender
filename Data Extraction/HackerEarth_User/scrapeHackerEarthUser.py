import json
from bs4 import BeautifulSoup

from json2html import *

import requests
import time
import pickle
import os
import json
import sys
import logging
import datetime
import time
import operator

from HackerEarthUser import HackerEarthUser


def fetch_submissions(link):

	try:
		submissionsList = []
		submissionsDict = {}
		languageDict = {}
			
		i = 1

		while True:
			URL  = link + '/?page='+str(i)
			#response = requests.get(URL, headers={'Host': 'www.hackerearth.com', 'Accept': '*/*', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://www.hackerearth.com/problems/activity/', 'Content-Type': 'application/json; charset=utf-8'})
			response = requests.get(URL, headers={ 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://www.hackerearth.com/submissions/'})
			page = json2html.convert(json = response.content)
			#print page
			soup = BeautifulSoup(page, "html.parser")

			problems = soup.findAll("a", { "class" : 'no-color hover-link' })
			if len(problems) == 0:
				break

			cols = [header.text for header in soup.find('thead').find('tr').findAll('td')]
			langTag = cols[5]
			
			col_idx = cols.index(langTag)
			languageList = [td[col_idx].string for td in [tr.findAll('td') for tr in soup.find('tbody').findAll('tr')]]
			#print languageList
			for language in languageList:
				if languageDict.has_key(language):
					languageDict[language] += 1
				else:
					languageDict[language] = 1
			
			
			for problem in problems:
				if submissionsDict.has_key(problem.text):
					submissionsDict[problem.text][0] += 1
				else:
					submissionsDict[problem.text] = [1]

				
			acProblemsURL  = link + '/?result=AC&page='+str(i)

			response = requests.get(acProblemsURL, headers={ 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://www.hackerearth.com/submissions/'})
			acProblemsPage = json2html.convert(json = response.content)
			acProblemsPage = BeautifulSoup(acProblemsPage, "html.parser")
			problems = acProblemsPage.findAll("a", { "class" : 'no-color hover-link' })
			datetimeList = acProblemsPage.findAll("a", { "class" : "hover-link gray-text tool-tip" })
			for datetime, problem in zip(datetimeList, problems):
				#print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(datetime['data-livestamp'])))
				#print str(problem.text) + " " + str(submissionsDict.has_key(problem.text))
				if submissionsDict.has_key(problem.text):
					if len(submissionsDict[problem.text]) == 1:
						submissionsDict[problem.text].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(datetime['data-livestamp']))))
				else:
					submissionsDict[problem.text] = [0]
					submissionsDict[problem.text].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(datetime['data-livestamp']))))
			
			#print "Success " + str(i)
			i += 1
		
		prefferedLanguage = max(languageDict.iteritems(), key=operator.itemgetter(1))[0]

		for submission in submissionsDict:
			if len(submissionsDict[submission]) == 2:
				submissionDetails = {"problemName" : submission, "submissionDate" : submissionsDict[submission][1], "submissionCount" : submissionsDict[submission][0]}
				submissionsList.append(submissionDetails)

	except Exception as e:
		submissionsList = Error
		prefferedLanguage = Error
		#print(e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print 'Exception at line '+ str(exc_tb.tb_lineno)
		logging.error('Time: {0} File: {1} Line: {2} Link: {3} Caused By: {4}'.format(datetime.datetime.now(), os.path.basename(__file__),
								exc_tb.tb_lineno, link, e))
		# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
		# 		' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))
	finally:
		return submissionsList, prefferedLanguage


def fetch_user(username, submissionslink):
	
	try:
		userProfileLink = 'https://www.hackerearth.com/@' + username
		response = requests.get(userProfileLink)
		profilePage = BeautifulSoup(response.text, "html.parser")
		
		nameTag = profilePage.findAll("h1", { "class" : 'name ellipsis larger' })
		name = nameTag[0].text

		try:
			locationTag = profilePage.findAll("div", { "class" : 'track-current-location icon-text regular light float-left' })
			location = locationTag[0].text.strip()
		except:
			location = "NA"

		try:
			education = "NA"
			educationtionTag = profilePage.findAll("div", { "class" : 'skill-snippet less-margin-2' })
			for tag in educationtionTag:
				if "Education:" in tag.text:
					education = tag.text.replace("Education:","").strip()
					break
		except:
			education = "NA"

		try:
			ratingPageLink = 'https://www.hackerearth.com/users/pagelets/' + username + '/coding-data/'
			response = requests.get(ratingPageLink)
			ratingPage = BeautifulSoup(response, "html.parser")
			ratingTag = ratingPage.findAll("a", { "class" : 'dark weight-700' })
			rating = ratingTag.text
		except:
			rating = "NA"
		#print name + " " + location + " " + education + " " + rating
		submissionsList, prefferedLanguage = fetch_submissions(submissionslink)

		user = HackerEarthUser(userProfileLink, username, name, location, education, rating, prefferedLanguage, submissionsList)

	except Exception as e:
		print(e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print 'Exception at line '+ str(exc_tb.tb_lineno)
		logging.error('Time: {0} File: {1} Line: {2} UserURL: {3} Caused By: {4}'.format(datetime.datetime.now(), os.path.basename(__file__),
								exc_tb.tb_lineno, userProfileLink, e))
		# logging.error(str(datetime.datetime.now()) + ' :File Name: '+ str(os.path.basename(__file__)) +
		# 		' :Line Number: '+ str(exc_tb.tb_lineno) +' :Caused By: ' + str(e))
		user = None
	finally:
		return user
	

if __name__ == '__main__':

	try:
		with open('texts/userList.txt') as listF:
			usernames = listF.read().splitlines()
			count = 0
			if os.path.exists('curr_progress'):
				with open('curr_progress', 'rb') as progRead:
					count = pickle.load(progRead)

			for i in range(count, 1000):
				with open('curr_progress', 'wb') as progWrite:
					pickle.dump(count, progWrite)
					count = count + 1
				
				user = fetch_user(usernames[i], 'https://www.hackerearth.com/AJAX/feed/newsfeed/submission/user/'+ usernames[i])
				#with open('users/' + usernames[i], 'wb') as userWrite:
				#	pickle.dump(user, userWrite)
				print('count = ' + str(count) + ' ' + str(usernames[i]))

	except Exception as e:
		print(e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print 'Exception at line '+ str(exc_tb.tb_lineno)
		logging.error('Time: {0} File: {1} Line: {2} Caused By: {3}'.format(datetime.datetime.now(), os.path.basename(__file__),
								exc_tb.tb_lineno, e))
