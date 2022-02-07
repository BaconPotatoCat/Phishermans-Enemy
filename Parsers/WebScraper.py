from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from urllib.request import urlopen
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import SSLError

import requests
import time
import re
import json

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
def getDomain(url, TLDs):
    regex = "https?://(www\.)?"
    for d in TLDs:
        if d in url:
            if re.search(regex, url):
                return url[re.search(regex, url).span()[1]:url.find(d)+4:]
        else:
            return "localhost"

def getPopup(url):
    try:
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options = options)
        driver.get(url)
        print("Waiting 5 seconds to see if an alert popup appears...")
        WebDriverWait(driver,5).until(EC.alert_is_present(), 'Timed out waiting for PA creation '
        + 'confirmation popup to appear.')
        alert = driver.switch_to.alert
        alert.send_keys("yes")
        alert.dismiss()
        driver.close()
        print("Alert box with text input detected.")
        return -1
    except ElementNotInteractableException:
        print("Alert box without text input detected.")
        return 1
    except TimeoutException:
        print("No alert")
        return 1
    except Exception as e:
        print(e)

def getHTML(url):
    try:
        formActions = list()
        reqURLs = list()
        anchors = list()
        page = requests.get(url, verify = False)
        html = page.content.decode("utf-8")
        reqRegex = "(src) ?\= ?([\'\"]\S*[\'\"])"
        anchorRegex = "(href) ?\= ?([\'\"]\S*[\'\"])"
        for line in html.split("\n"):
            if "form action" in line:
                formActions.append(line.strip()[line.find("=")+2:-3:])
            if " src" in line and not "<script" in line:
                reqURLs.append((re.search(reqRegex,line.strip()).group())[5:-1])
            if "<a href" in line:
                anchors.append((re.search(anchorRegex,line.strip()).group())[6:-1])
        return {"SFH":formActions, "RequestURL":reqURLs, "URL_of_Anchor": anchors}
    except Exception as e:
        print("HTML Error:",e)

def getAge(url):
    u = "https://input.payapi.io/v1/api/fraud/domain/age/"+url[4::]
    req = requests.get(u, verify = False)
    return json.loads(req.text)

def getSSL(url):
    try:
        requests.get(url)
        return 1
    except SSLError as e:
        # Website does not have valid SSL Certificate.
        return -1