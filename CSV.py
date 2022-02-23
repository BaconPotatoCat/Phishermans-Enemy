import csv
import os.path

columns = ["URL", "LongURL", "ShortURL", "Redirecting", "PrefixSuffix","SubDomains", "HTTPS", "RequestURL", "AnchorURL",
           "ServerFormHandler", "StatusBarCust","UsingPopupWindow", "AgeofDomain", "WebsiteTraffic", "Model", "Prediction"]

def savecsv(listOfDict):
    csv_file = "Past_Predictions.csv"
    try:
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            if not file_exists:
                writer.writeheader()  # file doesn't exist yet, write a header
            for data in listOfDict:
                writer.writerow(data)
    except IOError:
        print("The Past_Predictions.csv is currently open. Please close the file for Phisherman's Enemy to modify it.")

# parse in a url into here
def loadcsv(url):
    csv_file = "Past_Predictions.csv"
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
                        return i
            return False
        else:
            return False
    except FileExistsError:
        return False








