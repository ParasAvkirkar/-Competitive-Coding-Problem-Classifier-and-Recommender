from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime

import requests
from spojUser import SpojUser, SubmissionDetails
import pickle, sys, os
sys.path.append("../DataBase")
import sqlDB
import time


def fetch_user(userLink, driver):
	
	# baseUrl = "http://www.spoj.com/users/"
	# userLink = baseUrl + uname
	uname = userLink.split('/')[4]
	print uname

	driver.get(userLink)
	time.sleep(3)
	print('reach user page '+ userLink)

	try:
		profile = driver.find_element_by_id('user-profile-left')
		# try:
		# 	nameElm = profile.find_element_by_tag_name('h3')
		# 	name = nameElm.text
		# 	print(name)
		# except Exception as e:
		# 	print e
		# 	exc_type, exc_obj, exc_tb = sys.exc_info()
		# 	print 'Exception at line '+ str(exc_tb.tb_lineno) 
		# 	name = ""
		# 	print "name not found"
		
		pElms = profile.find_elements_by_tag_name('p')
		
		for p in pElms:
			try:
				countryElm = p.find_element_by_class_name('fa-map-marker')
				country = p.text
				print country.split(",")[0]
				break
			except Exception as e:
				print e
				exc_type, exc_obj, exc_tb = sys.exc_info()
				print 'Exception at line '+ str(exc_tb.tb_lineno) 
				country = ""

		if country == "":
			print "country does not exist"
		#print driver.text

		try:
			#rankElm = p.find_element_by_class_name('fa-trophy')
			bodyTag = driver.find_element_by_tag_name('body')
			html = bodyTag.text
			#World Rank: #39
			index = html.index('World Rank: ')
			bracketIndex = index + html[index:].index('(')
			print str(index + 13) + ' ' + str(bracketIndex)
			print html[index + 13: bracketIndex]
			rank = html[index + 13: bracketIndex]
			
			
			#re.sub("[^0-9, .]", "", allDataTags[2].text)
			pointIndex = bracketIndex + html[bracketIndex:].index('p')
			rating = html[bracketIndex + 1: pointIndex - 1]
			
			print rank
			print rating
			#break
		except Exception as e:
			print e
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print 'Exception at line '+ str(exc_tb.tb_lineno) 
			rank = ""		
		# for p in pElms:

		if rank == "":
			print "rank does not exist"		

		for p in pElms:
			try:
				institutionElm = p.find_element_by_class_name('fa-building-o')
				institution = p.text.split()[1]
				print institution
				break
			except Exception as e:
				print e
				exc_type, exc_obj, exc_tb = sys.exc_info()
				print 'Exception at line '+ str(exc_tb.tb_lineno) 
				institution = ""		

		if institution == "":
			print "institution does not exist"			
		
		probs = []
		submissionDetails = []
		try:
			probTable = driver.find_element_by_class_name('table-condensed')
			for prob in probTable.find_elements_by_tag_name('td'):
				# print prob.text + 'kuch'
				if len(prob.text) > 0:
					submissionTime = None
					#probs.append(prob.text)
					try:
						statusDriver.get(prob.find_element_by_tag_name('a').get_attribute('href'))
						print statusDriver.current_url
						dataTag = statusDriver.find_elements_by_class_name('status_sm')[0]
						submissionTime = datetime.strptime(dataTag.text,'%Y-%m-%d %H:%M:%S')
						print str(submissionTime)
						submissionDetails.append(SubmissionDetails(prob.text, None, submissionTime))
					except Exception as e:
						print e
						exc_type, exc_obj, exc_tb = sys.exc_info()
						print 'Exception at line '+ str(exc_tb.tb_lineno) 

		except Exception as e:
			print e
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print 'Exception at line '+ str(exc_tb.tb_lineno) 
			print "probs does not exist"

		lang = {}
		prefLang = ''
		driver.get(userLink.replace('users', 'status'))
		
		allDataTags = driver.find_elements_by_class_name('slang')
		for dataTag in allDataTags:
			l = dataTag.text
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
			# print l + 'arrow'
		
		prefLang = ""
		max = -1;
		for key in lang:
			if lang[key] > max:
				prefLang = key
				max = lang[key]

		print prefLang		
		
		user = SpojUser(userLink, uname, country, submissionDetails, rating, rank)

		sqlDB.insert_user_db("spoj_user", uname, country, country, True, submissionDetails, prefLang, rating, rank)
		# with open('users/' + uname, 'w+b') as f:
		# 	pickle.dump(user, f)


		
	except Exception as e:
		print('element not found')
		print(e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print 'Exception at line '+ str(exc_tb.tb_lineno) 
		prob = None
	else:
		pass
	finally:
		pass

# driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
# driver = webdriver.Chrome()
# statusDriver = webdriver.Chrome()
statusDriver = webdriver.Chrome('C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe')
count = 0

try:
	with open('curr_progress', 'r+b') as f:
		count = pickle.load(f)
		print count
except Exception as e:
	# print e
	exc_type, exc_obj, exc_tb = sys.exc_info()
	print 'Exception at line '+ str(exc_tb.tb_lineno) 
	count = 0		


i = 0
f = open('users_urls.txt', 'r')
for ulink in f:
	if count == i:
		ulink = ulink.split('\n')[0]
		fetch_user(ulink, driver)
		
		count += 1
		with open('curr_progress', 'w+b') as f:
			pickle.dump(count, f)

	i += 1	
	# print i, " ", count

driver.close()