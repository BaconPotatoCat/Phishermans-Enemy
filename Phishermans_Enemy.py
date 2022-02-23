import argparse
from WebScraper import *
from CSV import *
from Model.prediction import *
parser = argparse.ArgumentParser(description='Scrape information from a website/list of websites to determine if it is a phishing site.',
                    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='The URL to scan, inclusive of HTTP/HTTPS. (Required)', metavar='[URL]',required=True)
parser.add_argument('-m', '--model', help='The model to be used for predicting the outcome.\n1 - GBC\n2 - RFC\n3 - XGB', metavar='[MODEL NUM]', default=1)

args = parser.parse_args()

if args.url:
    url = args.url
    model = int(args.model)
    runPredict = False
    if model < 1 or model > 3:
        exit(-1)
    if loadcsv(url):
        print("Existing prediction for URL.")
        rerun = input("Would you like to run a new prediction on the URL? [y/n]\n")
        if rerun == "y":
            runPredict = True
        else:
            print("Existing data is:")
            print(loadcsv(url))
    else:
        runPredict = True
    if runPredict:
        data = {"LongURL": 1, "ShortURL": 1, "Redirecting": 1, "PrefixSuffix": 1,
                "SubDomains": 1, "HTTPS": 1, "RequestURL": 1, "AnchorURL": 1, "ServerFormHandler": 1, "StatusBarCust": 1,
                "UsingPopupWindow": 1, "AgeofDomain": 1, "WebsiteTraffic": 1}
        domain = getDomain(url)
        # Get AgeofDomain attribute
        if "error" not in getAge(domain):
            age = getAge(domain)["result"]
            if age < 180:
                data["AgeofDomain"] = -1
        else:
            data["AgeofDomain"] = -1
        # Get LongURL attribute
        if len(url) > 75:
            data["LongURL"] = -1
        elif len(url) > 53:
            data["LongURL"] = 0
        # Get ShortURL attribute
        if domain == "tinyurl.com" or domain == "bit.ly":
            data["ShortURL"] = -1
        #Get ServerFormHandler, RequestURL, AnchorURL, and StatusBarCust attributes
        HTML = getHTML(url)
        #data["UsingPopupWindow"] = getPopup(url)
        if HTML:
            data["ServerFormHandler"] = HTML["SFH"]
            data["RequestURL"] = HTML["RequestURL"]
            data["AnchorURL"] = HTML["URL_of_Anchor"]
            data["StatusBarCust"] = HTML["StatusBarCust"]
        data["PrefixSuffix"] = getPreffixSuffix(url)
        data["WebsiteTraffic"] = web_traffic(url)
        data["SubDomains"] = getSubDomain(url)
        data["Redirecting"] = checkRedirect(url)
        data["HTTPS"] = checkSSL(url)
        data["Prediction"] = predict(model,[data])[0]
        data["URL"] = url
        data["Model"] = model
        savecsv([data])
        print("\n",data)