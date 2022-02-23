#!/usr/bin/env python
# coding: utf-8
import csv
import os.path


# Can delete as using this as sample testing
url1 = "www.yahoo.com"

# parse in a url into here
def loadcsv(url):
    csv_file = "passPredict.csv"
    try:
        file_exists = os.path.isfile(csv_file)
        if file_exists:
            reader = csv.DictReader(open(csv_file, 'r'))
            d = list(reader)
        for i in d:
            for x,y in i.items():
                if y == url:
                    # prints can be deleted as parsing as sample testing true false be used only 
                    # entire chunk of code here can be used to return back the values if so desired so leaving within here
                    print(y)
                    print(i["Prediction"])
                    return True

    except FileExistsError:
        return False


def main():
    # modify here into main to select if we are going to predict
    if loadcsv(url1):
        print("Prediction Exists")
    else:
        print("Continue to predict the url")


if __name__ == "__main__":
    main()











