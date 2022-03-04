import argparse
from WebScraper import *
from CSV import *
from Model.prediction import *
parser = argparse.ArgumentParser(description='Scrape information from a website/list of websites to determine if it is a phishing site.',
                    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-u', '--url', help='The URL to scan, inclusive of HTTP/HTTPS. (Required)', metavar='[URL]',required=True)
parser.add_argument('-m', '--model', help='The model to be used for predicting the outcome.\n1 - GBC\n2 - RFC\n3 - XGB', metavar='[MODEL NUM]', default=1)

def runPredict(url, model):
    try:
        data = {"LongURL": 1, "ShortURL": 1, "Redirecting": 1, "PrefixSuffix": 1,
                "SubDomains": 1, "HTTPS": 1, "RequestURL": 1, "AnchorURL": 1, "ServerFormHandler": 1, "StatusBarCust": 1,
                "AgeofDomain": 1, "WebsiteTraffic": 1}
        domain = getDomain(url, 1)
        subdoms = (getDomain(url, 3) + '.' + domain).split('.')
        subdom = ""
        age = 0
        for sd in subdoms[:-1:]:
            subdom += sd + '.'
        subdom = subdom.strip(".")
        # Get AgeofDomain attribute
        if "dataError" not in getAge(url)['WhoisRecord']:
            cdate = getAge(url)['WhoisRecord']['createdDate'][:10:].split('-')
            createdate = datetime.date(int(cdate[0]), int(cdate[1]), int(cdate[2]))
            age = (datetime.date.today() - createdate).days
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
        # Get ServerFormHandler, RequestURL, AnchorURL, and StatusBarCust attributes from HTML of URL
        HTML = getHTML(url)
        if HTML:
            data["ServerFormHandler"] = HTML["SFH"][0]
            data["RequestURL"] = HTML["RequestURL"][0]
            data["AnchorURL"] = HTML["URL_of_Anchor"][0]
            data["StatusBarCust"] = HTML["StatusBarCust"][0]
        data["PrefixSuffix"] = getPreffixSuffix(url)
        data["WebsiteTraffic"] = web_traffic(url)[0]
        data["SubDomains"] = getSubDomain(subdom)
        data["Redirecting"] = checkRedirect(getDomain(url, 4))
        data["HTTPS"] = checkSSL(url)[0]
        # Generate prediction based off data
        data["Prediction"] = predict(int(model),[data])[0]
        # Update data to contain original values scraped for report generation
        data["LongURL"] = (0,len(url))
        if data["Redirecting"] == -1:
            data["Redirecting"] = (-1, url.find("//"))
        if data["PrefixSuffix"] == -1:
            index = list()
            for count, char in enumerate(url):
                if char == "-":
                    index.append(count)
            data["PrefixSuffix"] = (-1, index)
        if data["SubDomains"] != 1:
            index = list()
            for count, char in enumerate(subdom):
                if char == ".":
                    index.append(count)
            data["SubDomains"] = (data["SubDomains"], subdom.count('.'), index)
        if data["HTTPS"] != 1:
            data["HTTPS"] = checkSSL(url)
        if data["ServerFormHandler"] != 1:
            data["ServerFormHandler"] = HTML["SFH"]
        if data["RequestURL"] != 1:
            data["RequestURL"] = HTML["RequestURL"]
        if data["AnchorURL"] != 1:
            data["AnchorURL"] = HTML["URL_of_Anchor"]
        if data["StatusBarCust"] != 1:
            data["StatusBarCust"] = HTML["StatusBarCust"]
        if data["AgeofDomain"] != 1:
            if "dataError" not in getAge(url)['WhoisRecord']:
                data["AgeofDomain"] = (data["AgeofDomain"], age)
            else:
                data["AgeofDomain"] = (data["AgeofDomain"], "Unable to retrieve domain age.")
        if data["WebsiteTraffic"] != 1:
            data["WebsiteTraffic"] = web_traffic(url)
        data["URL"] = url
        data["Model"] = int(model)
        savecsv([data])
        print("Prediction complete.")
        return 1
    except Exception as e:
        print("Error occured:\n", e)
        return -1

def checkPrediction(url, model):
    # Checks Past_Predictions.csv if URL and model already exists
    if model < 1 or model > 3:
        exit(-1)
    if loadcsv(url):
        print("Existing prediction for URL.")
        return 0
    else:
        return 1

if __name__ == "__main__":
    args = parser.parse_args()
    if args.url:
        url = args.url
        model = int(args.model)
        if not checkPrediction(url, model):
            rerun = ""
            while rerun != "y" or rerun != "n":
                rerun = input("Would you like to run a new prediction on the URL? [y/n]\n")
                if rerun == "y":
                    runPredict(url, model)
                    break
                elif rerun == "n":
                    print("Existing data is:\n")
                    print(loadcsv(url))
                    break
        else:
            runPredict(url, model)
    else:
        print("No URL")