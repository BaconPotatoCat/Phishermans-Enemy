import argparse
from Parsers.WebScraper import *
parser = argparse.ArgumentParser(description='Scrape information from a website/list of websites to determine if it is a phishing site.')
parser.add_argument('-u', '--url', help='The URL to scan. (Required)', metavar='www.google.com', required=True)

args = parser.parse_args()

if args.url:
    url = args.url
    rootdomains = (".com",".org",".net",".gov",".edu")
    domain = ""
    for d in rootdomains:
        if args.url.find(d) != -1:
            if args.url.find("www.") != -1:
                domain = args.url[args.url.find("www."): args.url.find(d)+4]
            elif args.url.find("http") != -1:
                domain = args.url[args.url.find("http"): args.url.find(d)+4]
        else:
            domain = "localhost"
    SFActions = getSFH(url)
    if len(SFActions) > 0:
        emptySFA = False
        for action in SFActions:
            if len(action) == 0 and not emptySFA:
                print("Webpage has %d form(s) with an empty form action."%(SFActions.count(action)))
                emptySFA = True
            if len(action) > 0 and domain not in action and action[0] != "/":
                print("Webpage has form leading to external domain: %s"%(action))