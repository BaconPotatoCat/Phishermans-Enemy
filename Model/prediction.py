#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd

def predict(model, listOfDict):
    if model == 1:
        # Gradient Boosting Algorithm #
        val_x = pd.DataFrame.from_dict(listOfDict, orient='columns')
        GBC = pickle.load(open("Model/train_GBC_model.sav", 'rb'))
        z = GBC.predict(val_x)
        return z
    elif model == 2:
        # Random Forest Classifier #
        val_x = pd.DataFrame.from_dict(listOfDict, orient='columns')
        RFC = pickle.load(open("Model/train_rfc_model.sav", 'rb'))
        z = RFC.predict(val_x)
        return z
    elif model == 3:
        # XGB Classifier #
        val_x = pd.DataFrame.from_dict(listOfDict, orient='columns')
        xgb = pickle.load(open("Model/train_xgb_model.sav", 'rb'))
        z = xgb.predict(val_x)
        return z
    else:
        return "Error in model selection"
