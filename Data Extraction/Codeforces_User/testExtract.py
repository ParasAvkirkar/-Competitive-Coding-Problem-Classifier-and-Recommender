from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from codeforcesuser import CodeForcesUser
from scrapeCodeForceUser import fetch_user
import requests
import json
import pickle

# user = fetch_user('http://codeforces.com/api/user.info?handles=TooDifficuIt;')
# print user
# response = requests.get('http://codeforces.com/api/user.info?handles=TooDifficuIt;')
# print(response.content)


with open('temp', 'wb') as f:
	pickle.dump('paras', f)

with open('temp', 'rb') as f:
	temp = pickle.load(f)
	print(temp)