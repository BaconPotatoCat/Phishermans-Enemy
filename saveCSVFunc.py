#!/usr/bin/env python
# coding: utf-8
import csv
import os.path


columns = ["URL", "LongURL", "ShortURL", "Redirecting", "PrefixSuffix","SubDomains", "HTTPS", "RequestURL", "AnchorURL", "ServerFormHandler", "StatusBarCust","UsingPopupWindow", "AgeofDomain", "WebsiteTraffic", "Prediction"]


listOfDict1 = [{"URL": "www.google.com", "Prediction": 1, "ShortURL": 1, "LongURL": 1, "Redirecting": 1, "PrefixSuffix": 1, "SubDomains": 0, "HTTPS": -1,"RequestURL": 1, "AnchorURL": 0, "ServerFormHandler": -1, "StatusBarCust": 1, "UsingPopupWindow": 1, "AgeofDomain": -1,"WebsiteTraffic": 0}]


def savecsv(listOfDict):
    csv_file = "passPredict.csv"
    try:
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            if not file_exists:
                writer.writeheader()  # file doesn't exist yet, write a header
            for data in listOfDict:
                writer.writerow(data)
    except IOError:
        print(IOError)


def main():
    savecsv(listOfDict1)


if __name__ == "__main__":
    main()











