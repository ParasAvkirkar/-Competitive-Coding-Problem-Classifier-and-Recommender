from selenium import webdriver
from user import User
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import requests
from spojUser import SpojUser
import pickle



def fetch_user(userLink, driver):
	
	# baseUrl = "http://www.spoj.com/users/"
	# userLink = baseUrl + uname
	uname = userLink.split('/')[4]
	print uname

	driver.get(userLink)
	print('reach user page '+ userLink)

	try:
		profile = driver.find_element_by_id('user-profile-left')
		try:
			nameElm = profile.find_element_by_tag_name('h3')
			name = nameElm.text
			print(name)
		except Exception as e:
			name = ""
			print "name not found"
		
		pElms = profile.find_elements_by_tag_name('p')
		
		for p in pElms:
			try:
				countryElm = p.find_element_by_class_name('fa-map-marker')
				country = p.text
				print country.split(",")[0]
				break
			except Exception as e:
				country = ""

		if country == "":
			print "country does not exist"


		for p in pElms:
			try:
				rankElm = p.find_element_by_class_name('fa-trophy')
				temp = p.text.split("#")[1]
				rank = temp.split()[0]
				rating = temp.split("(")[1].split()[0]
				print rank
				print rating
				break
			except Exception as e:
				rank = ""		

		if rank == "":
			print "rank does not exist"		

		for p in pElms:
			try:
				institutionElm = p.find_element_by_class_name('fa-building-o')
				institution = p.text.split()[1]
				print institution
				break
			except Exception as e:
				institution = ""		

		if institution == "":
			print "institution does not exist"			
		
		probs = []
		try:
			probTable = driver.find_element_by_class_name('table-condensed')
			for prob in probTable.find_elements_by_tag_name('td'):
				probs.append(prob.text)

		except Exception as e:
			print "probs does not exist"


		user = SpojUser(userLink, uname, name, country, probs, rating, rank)
		with open('users/' + uname, 'w+b') as f:
			pickle.dump(user, f)

		# with open('users/' + uname, 'r+b') as f2:
		# 	n = pickle.load(f2)
		# 	print n.name
		

		
	except Exception as e:
		print('element not found')
		print(e)
		prob = None
	else:
		pass
	finally:
		pass

driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

count = 0

try:
	with open('curr_progress', 'r+b') as f:
		count = pickle.load(f)
		print count
except Exception as e:
	# print e
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