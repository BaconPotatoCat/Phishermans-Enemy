import pandas as pd
from flask import Flask, render_template, request, redirect, jsonify

def getRow(url):
    selectedrow = []
    prevrow = prev.iloc[int(url)]
    selectedrow = prevrow.values.flatten().tolist()
    return selectedrow

app = Flask(__name__)
prev = pd.read_csv("Past_Predictions.csv", dtype="str")
prevd = prev.to_dict()

# Get the list of all urls
li = []
phish=0
legit=0
for i in prevd["URL"]:
    li.append(prevd["URL"][i])
for i in prevd["Prediction"]:
    if prevd["Prediction"][i] == "1":
        legit+=1
    else:
        phish+=1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
    if request.method == "POST":
        # Get the urls which match the search input
        if request.form.get("query") is not None:
            search_input = request.form.get("query")
            data = []
            for index, value in enumerate(li):
                if search_input in value:
                    data.append(tuple((index,value)))
            return jsonify(data)
        # If the search is blank display all urls in the file
        else:
            values = list(enumerate(li))
            return jsonify(values)

@app.route("/detailed", methods=["GET","POST"])
def detailed():
    if request.method == "POST":
        # Return the info of selected url
        selectedURL = request.form.get("row")
        details = getRow(selectedURL)
        details.append(legit)
        details.append(phish)
        return jsonify(details)
    else:
        return jsonify("Error")

if __name__ == "__main__":
    app.run(host="0.0.0.0")