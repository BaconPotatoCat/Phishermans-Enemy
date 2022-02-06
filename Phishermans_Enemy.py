import argparse
from Parsers.WebScraper import *
parser = argparse.ArgumentParser(description='Scrape information from a website/list of websites to determine if it is a phishing site.')
parser.add_argument('-u', '--url', help='The URL to scan, inclusive of HTTP/HTTPS. (Required)', metavar='https://www.google.com', required=True)

args = parser.parse_args()

if args.url:
    url = args.url
    extUrls = 0
    susAnchors = 0
    TLDs = (".com", ".org", ".net", ".int", ".gov", ".edu")
    data = {"Popup": 1, "SFH": 1, "HTTPS (SSL)": 1, "RequestURL": 1, "URL_of_Anchor": 1, "WebsiteTraffic": 1,
            "AgeofDomain": 1, "SubDomains": 1, "UsingIP": 1, "URL_Length": 1}

    domain = getDomain(url, TLDs)
    data["Popup"] = getPopup(url)
    SFActions = getHTML(url)["SFH"]
    if len(SFActions) > 0:
        for action in SFActions:
            if len(action) == 0:
                print("Webpage has a form with an empty form action.")
                data["SFH"] = -1
                break
            if len(action) > 0 and action[0] != "/":
                print("Webpage has form leading to external domain: %s"%(action))
                data["SFH"] = 0
            elif len(action) > 0:
                print("Webpage has legitimate form action: %s" % (action))
    reqURLs = getHTML(url)["RequestURL"]
    if len(reqURLs) > 0:
        for u in reqURLs:
            for tld in TLDs:
                # if URL has a top level domain, it is not a local link.
                # check if the URL belongs to an external domain.
                if tld in u and domain not in u:
                    extUrls += 1
        if extUrls / len(reqURLs) > 61/100:
            data["RequestURL"] = -1
        elif extUrls / len(reqURLs) > 11/50:
            data["RequestURL"] = -0
    if "error" not in getAge(domain):
        age = getAge(domain)["result"]
        if age < 180:
            data["AgeofDomain"] = -1
    else:
        data["AgeofDomain"] = -1
    if len(url) > 75:
        data["URL_Length"] = -1
    elif len(url) > 53:
        data["URL_Length"] = 0
    URLAnchors = getHTML(url)["URL_of_Anchor"]

    if len(URLAnchors) > 0:
        for a in URLAnchors:
            for tld in TLDs:
                if tld in a and domain not in a:
                    susAnchors += 1
                elif a == "#":
                    susAnchors += 1
                #elif ":void(0)" in a:
                    #susAnchors += 1

        if susAnchors / len(URLAnchors) > 67/100:
            data["URL_of_Anchor"] = -1
        elif susAnchors / len(URLAnchors) > 31/100:
            data["URL_of_Anchor"] = -0
    data["HTTPS (SSL)"] = getSSL(url)
    print(data)