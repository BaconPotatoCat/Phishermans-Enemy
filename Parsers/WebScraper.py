from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from urllib.request import urlopen
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from tldextract import extract
import OpenSSL.SSL

import requests
import re
import json
import ipaddress
import ssl
import socket
import datetime

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
def getDomain(url):
    if extract(url).suffix:
        return extract(url).domain + '.' + extract(url).suffix
    else:
        return extract(url).domain

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
        formRegex = "(form .*action) ?\= ?([\'\"]\S*[\'\"])"
        reqRegex = "(src) ?\= ?([\'\"]\S*[\'\"])"
        anchorRegex = "(href) ?\= ?([\'\"]\S*[\'\"])"
        for line in html.split("\n"):
            if "form action" in line:
                formActions.append((re.search(formRegex,line.strip()).group(2)[1:-1]))
            if " src" in line and not "<script" in line:
                reqURLs.append((re.search(reqRegex,line.strip()).group(2))[1:-1])
            if "<a href" in line:
                anchors.append((re.search(anchorRegex,line.strip()).group(2))[1:-1])
        return {"SFH":formActions, "RequestURL":reqURLs, "URL_of_Anchor": anchors}
    except Exception as e:
        print("HTML Error:",e)

def getAge(url):
    u = "https://input.payapi.io/v1/api/fraud/domain/age/"+url[4::]
    req = requests.get(u, verify = False)
    return json.loads(req.text)

def web_traffic(url):
    rank = BeautifulSoup(urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml")
    if not rank.find("REACH") == None:
        rank = int(rank.find("REACH")['RANK'])
        if rank:
            if rank < 100000:
                return 1
            elif rank > 100000:
                return 0
    else:
        return -1
    
def getIfIP(url):
    try:
        ipaddress.ip_address(url)
        return -1
    except ValueError as e:
        print(e)
        return 1

def getSubDomain(url):
    sd = extract(url).subdomain
    if sd.count('.') == 0:
        return 1
    elif sd.count('.') == 1:
        return 0
    else:
        return -1

def checkSSL(url):
    try:
        if url[:8] != "https://":
            return -1
        if extract(url).subdomain:
            url = extract(url).subdomain + '.' + getDomain(url)
        else:
            url = getDomain(url)
        ssl_date = r"%b %d %H:%M:%S %Y %Z"
        context = ssl.create_default_context()
        connection = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=url, )
        connection.settimeout(3.0)
        connection.connect((url, 443))
        ssl_info = connection.getpeercert()
        expiry = datetime.datetime.strptime(ssl_info["notAfter"], ssl_date)
        issued = datetime.datetime.strptime(ssl_info["notBefore"], ssl_date)
        remaining = expiry - datetime.datetime.utcnow()
        year = datetime.timedelta(days=365)
        ssl_connection_setting = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
        ssl_connection_setting.set_timeout(5)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((url, 443))
            c = OpenSSL.SSL.Connection(ssl_connection_setting, s)
            c.set_tlsext_host_name(str.encode(url))
            c.set_connect_state()
            c.do_handshake()
            cert = c.get_peer_certificate()
            c.shutdown()
            s.close()
        if (datetime.datetime.utcnow() - issued <= year):
            return 0
        else:
            return 1
    except ssl.SSLCertVerificationError:
        # Invalid SSL Cert, Issuer not trusted
        ssl_connection_setting = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
        ssl_connection_setting.set_timeout(5)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((url, 443))
            c = OpenSSL.SSL.Connection(ssl_connection_setting, s)
            c.set_tlsext_host_name(str.encode(url))
            c.set_connect_state()
            c.do_handshake()
            cert = c.get_peer_certificate()
            c.shutdown()
            s.close()
        if cert.has_expired():
            return -1
        else:
            return 0