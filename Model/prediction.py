#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd


columns = ["LongURL", "ShortURL", "Redirecting", "PrefixSuffix","SubDomains", "HTTPS", "RequestURL", "AnchorURL", "ServerFormHandler", "StatusBarCust","UsingPopupWindow", "AgeofDomain", "WebsiteTraffic"]


model1 = int(input("Input model number: "))
listOfDict1 = [{"LongURL": 1, "ShortURL": 1, "Redirecting": 1, "PrefixSuffix": 1, "SubDomains": 0, "HTTPS": -1,"RequestURL": 1, "AnchorURL": 0, "ServerFormHandler": -1, "StatusBarCust": 1, "UsingPopupWindow": 1, "AgeofDomain": -1,"WebsiteTraffic": 0}]


def predict(model, listOfDict):
    if model == 1:
        # Gradient Boosting Algorithm #
        val_x = pd.DataFrame.from_dict(listOfDict, orient='columns')
        GBC = pickle.load(open("train_GBC_model.sav", 'rb'))
        z = GBC.predict(val_x)
        return z
    elif model == 2:
        # Random Forest Classifier #
        val_x = pd.DataFrame.from_dict(listOfDict, orient='columns')
        RFC = pickle.load(open("train_rfc_model.sav", 'rb'))
        z = RFC.predict(val_x)
        return z
    elif model == 3:
        # XGB Classifier #
        val_x = pd.DataFrame.from_dict(listOfDict, orient='columns')
        xgb = pickle.load(open("train_xgb_model.sav", 'rb'))
        z = xgb.predict(val_x)
        return z
    else:
        return "Error in model selection"



x = predict(model1, listOfDict1)
print(x)
