from selenium import webdriver
from user import User
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from user import User, UserSubmission


import requests
import pickle

import sys, os
sys.path.append("../DataBase")
sys.path.append("../Utilities")
import sqlDB
from driverUtil import getDriver

def fetch_user(uname, driver, statusPageDriver):
	
	baseUrl = "https://www.codechef.com/users/"
	userLink = baseUrl + uname

	driver.get(userLink)
	#wait = WebDriverWait(driver, 10)
	print('reach user page '+ userLink)

	try:
		try:
			countryElm = driver.find_element_by_class_name('user-country-name')
			country = countryElm.text
		except Exception as e:
			print (e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print exc_tb.tb_lineno
			country = ""
		print(country)


		allTrs = driver.find_elements_by_tag_name('tr')
		isStudent = False
		userCity = ''
		for tr in allTrs:
			tdTags = tr.find_elements_by_tag_name('td')
			if tdTags is not None and len(tdTags) == 2:
				if tdTags[0] is not None and 'student' in tdTags[0].text.lower():
					if 'student' in tdTags[1].text.lower():
						isStudent = True
					else:
						isStudent = False

				if 'city' in tdTags[0].text.lower():
					userCity = tdTags[1].text


		print(str(isStudent) + ' '  + userCity)
		rating_table = driver.find_element_by_class_name('rating-table')		

		#Get the problems solved
		problemsSolved = []
		userSubmissions = []
		countProbs = 0

		divOfTable = driver.find_element_by_class_name('profile')
		rowTags = divOfTable.find_elements_by_tag_name('tr')

		try:
			for rowTag in rowTags:
				allDataTags = rowTag.find_elements_by_tag_name('td')
				if 'success' in allDataTags[0].text.lower():
					aTags = allDataTags[1].find_elements_by_tag_name('a')
					for aTag in aTags:
						if aTag.get_attribute('href') is not None and 'status' in aTag.get_attribute('href'):
							problemCode = aTag.text
							noOfSubmission = 0
							time = None

							#driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
							
							countProbs = countProbs + 1
							flag = True
							statusUrl = aTag.get_attribute('href')
							try:
								while flag:
									statusPageDriver.get(statusUrl)
									tableTagStatus = statusPageDriver.find_element_by_class_name('dataTable')
									bodyTagStatus = tableTagStatus.find_element_by_tag_name('tbody')
									rowTagsStatus = bodyTagStatus.find_elements_by_tag_name('tr')
									allDataTagsStatus = rowTagsStatus[0].find_elements_by_tag_name('td')
									# print 'no of submission '+str(noOfSubmission) + ' row tag length'
									# for r in rowTagsStatus:
									# 	print r
									noOfSubmission = noOfSubmission + len(rowTagsStatus)
									if time is None:
										#10:57 PM 08/10/15
										time = datetime.strptime(allDataTagsStatus[1].text,'%I:%M %p %d/%m/%y')

									aTagsStatus = statusPageDriver.find_elements_by_tag_name('a')
									flag = False
									for aTagStatus in aTagsStatus:
										if aTagStatus.get_attribute('href') is not None and 'status' in aTagStatus.get_attribute('href'):
											imgTag = aTagStatus.find_element_by_tag_name('img')
											if 'next' in imgTag.get_attribute('src'):
												statusUrl = aTagStatus.get_attribute('href')
												flag = True
												break
							except Exception as e:
								print (e)
								exc_type, exc_obj, exc_tb = sys.exc_info()
								print exc_tb.tb_lineno


							#driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 
							
							userSubmissions.append( UserSubmission(problemCode, noOfSubmission, time))
							print "len: " + str(userSubmissions[len(userSubmissions)-1])
					break		
		except Exception as e:
			print (e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print exc_tb.tb_lineno



		# for p in problemsSolved:
		# 	print(p)
		print('work till getting problems')
		
		#Get rank and ratings
		rank = {'Long' : [], 'Short' : [], 'LTime' : []}
		rating = {'Long' : [], 'Short' : [], 'LTime' : []}
		
		count = 1
		for tr in rating_table.find_elements_by_tag_name('tr'):
			if count == 1:
				count += 1
				continue
				
			elif count == 2 :
				tds = tr.find_elements_by_tag_name('td')
				rank['Long'] = tds[1].text
				rating['Long'] = tds[2].text
				#print rating['Long']

			elif count == 3 :
				tds = tr.find_elements_by_tag_name('td')
				rank['Short'] = tds[1].text
				rating['Short'] = tds[2].text
				#print rating['Short']	

			elif count == 4 :
				tds = tr.find_elements_by_tag_name('td')
				rank['LTime'] = tds[1].text
				rating['LTime'] = tds[2].text
				#print rating['LTime']		
					
			count += 1

		
		for key in rating:
			rating[key] = rating[key].replace('(?)', '')
			print(str(rating[key]))
		# print(len(rating))
		count = 1
		lang = {}


		#Get preferred language		
		dataTable = driver.find_element_by_class_name('dataTable')
		for tr in dataTable.find_elements_by_tag_name('tr'):
			if count == 1:
				count += 1
				continue

			tds = tr.find_elements_by_tag_name('td')
			l = tds[3].text
			l = l.strip().lower()
			if 'c++' in l:
					l = 'c++'
			elif 'pas' in l:
					l = 'pas'
			elif 'pyth' in l:
					l = 'python'
			if l in lang:
					lang[l] += 1
			else:
				lang[l] = 0

		prefLang = ""
		max = -1
		for key in lang:
			if lang[key] > max:
				prefLang = key
				max = lang[key]

		print prefLang		


		u = User(uname, country, userCity, isStudent, userSubmissions, prefLang, rating, rank)
		#u.insert_db(uname, country, userCity, isStudent, userSubmissions, prefLang, rating, rank)
		sqlDB.insert_user_db('codechef_user', uname, country, userCity, isStudent, userSubmissions, prefLang, rating, rank)
		# with open('users/' + uname, 'w+b') as f:
		# 	pickle.dump(u, f)


		# with open('users/' + uname, 'r+b') as f2:
		# 	us = pickle.load(f2)
		# 	print "his name is " + us.uname + " city "
		# 	print us.probs	


	except Exception as e:
		print(e)
		# print('element not found')
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print exc_tb.tb_lineno
		prob = None
	else:
		pass
	finally:
		pass

#driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
# driver = webdriver.Chrome()
# driver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
# driver = None
# paths = ['', 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', 'C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe']
# i = 0
# while driver is None:
# 	try:
# 		driver = webdriver.Chrome(paths[i])
# 	except:
# 		pass
# 	i = i + 1
driver = getDriver()


#statusPageDriver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
# driver = webdriver.Chrome()
#fetch_user('anudeep2011', driver)
# fetch_user('paras18', driver)
# fetch_user('paragpachpute', driver)
# fetch_user('pranay0007', driver)
statusPageDriver = getDriver()

count = 0

try:
	with open('curr_progress', 'r+b') as f:
		count = pickle.load(f)
		print count
except Exception as e:
	# print e
	count = 0		


i = 0

f = open('users_ids.txt', 'r')
for uname in f:
	if count == i:
		uname = uname.split('\n')[0]
		fetch_user(uname, driver, statusPageDriver)

		count += 1
		with open('curr_progress', 'w+b') as f:
			pickle.dump(count, f)

	i += 1
# 	# print i, " ", count

# fetch_user('rahulj15', driver, statusPageDriver)
driver.close()

	