from selenium import webdriver
from user import User
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import requests
import pickle
from user import User

def fetch_user(uname, driver):
	
	baseUrl = "https://www.codechef.com/users/"
	userLink = baseUrl + uname

	driver.get(userLink)
	#wait = WebDriverWait(driver, 10)
	print('reach user page '+ userLink)

	try:
		countryElm = driver.find_element_by_class_name('user-country-name')
		country = countryElm.text
		# print(countryElm.text)

		print(country)

		#Get the city and student/professional
		#tableTag = driver.find_elements_by_tag_name('table')
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
		countProbs = 0
		aTags = driver.find_elements_by_tag_name('a')
		for aTag in aTags:
			if aTag.get_attribute('href') is not None and 'status' in aTag.get_attribute('href'):
				problemsSolved.append(aTag.text)
				countProbs = countProbs + 1
				#print(str(countProbs))

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
		print(len(rating))
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
			if l in lang:
				lang[l] += 1
			else:
				lang[l] = 0	


		prefLang = ""
		max = -1;
		for key in lang:
			if lang[key] > max:
				prefLang = key

		print prefLang		

		u = User(uname, country, userCity, isStudent, problemsSolved, prefLang, rating, rank)
		u.insert_db(uname, country, userCity, isStudent, problemsSolved, prefLang, rating, rank)
		
		with open('users/' + uname, 'w+b') as f:
			pickle.dump(u, f)


		# with open('users/' + uname, 'r+b') as f2:
		# 	us = pickle.load(f2)
		# 	print "his name is " + us.uname + " city "
		# 	print us.probs	


	except Exception as e:
		print(e)
		print('element not found')
		prob = None
	else:
		pass
	finally:
		pass

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
# driver = webdriver.Chrome()
#fetch_user('anudeep2011', driver)
# fetch_user('paras18', driver)
# fetch_user('paragpachpute', driver)
# fetch_user('pranay0007', driver)

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
		fetch_user(uname, driver)
		
		count += 1
		with open('curr_progress', 'w+b') as f:
			pickle.dump(count, f)

	i += 1	
	# print i, " ", count


driver.close()

	