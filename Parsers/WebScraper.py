from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib.request import urlopen
import time

def getPopup(url):
    try:
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options = options)
        driver.get(url)
        print("Waiting 5 seconds to see if an alert popup appears...")
        time.sleep(5)
        driver.close()
        return False
    except UnexpectedAlertPresentException as e:
        print("This webpage has an alert.")
        print(e.msg.split('\n')[0])
        return True
    except Exception as e:
        print(e)

def getSFH(url):
    try:
        formActions = list()
        page = urlopen(url)
        html = page.read().decode("utf-8")
        for line in html.split("\n"):
            if "form action" in line:
                formActions.append(line[line.find("=")+2:-3:])
        return formActions
    except Exception as e:
        print("HTML Error:",e)