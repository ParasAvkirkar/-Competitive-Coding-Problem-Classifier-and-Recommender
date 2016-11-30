__author__ = 'Pranay'

from selenium import webdriver

def getDriver():
    driver = None
    paths = ['', 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', 'C:\Users\Pranay\Downloads\Setups\Drivers\chromedriver.exe']
    i = 0
    while driver is None:
        try:
            driver = webdriver.Chrome(paths[i])
        except:
            pass
        i = i + 1
    return driver