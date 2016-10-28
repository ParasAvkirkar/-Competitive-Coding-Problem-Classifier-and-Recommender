from selenium import webdriver
from problems import Problem
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from CodechefProblemPage import getCodechefProblem


codechefUrl = 'https://www.codechef.com'
with open('problemsIr.txt') as f:
	for line in f:
		p = getCodechefProblem(codechefUrl + '/problems/' + line)
		if p == None:
			print('problem not got')
		else:
			print(p)
			