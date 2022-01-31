from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
import argparse, time

parser = argparse.ArgumentParser(description='Scrape information from a website/list of websites to determine if it is a phishing site.')
parser.add_argument('-u', '--url', help='The URL to scan. (Required)', metavar='www.google.com', required=True)

args = parser.parse_args()
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
        print("AH:",e.msg.split('\n')[0])
        return True
    except Exception as e:
        print(e)

if args.url:
    url = args.url
    print(args.url)
    print(getPopup(url))
