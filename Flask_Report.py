import pandas as pd
from flask import Flask, render_template, request, redirect, jsonify

def getRow(url):
    selectedrow = []
    prevrow = prev.loc[prev["URL"]==url]
    selectedrow = prevrow.values.flatten().tolist()
    return selectedrow

app = Flask(__name__)
prev = pd.read_csv("Past_Predictions.csv")
prevd = prev.to_dict()
li = []
for i in prevd["URL"]:
    li.append(prevd["URL"][i])

@app.route("/")
def index():
    return render_template("index.html",prev=prevd)

@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
    if request.method == "POST":
        if request.form.get("query") is not None:
            search_input = request.form.get("query")
            test = []
            for index, value in enumerate(li):
                if search_input in value:
                    test.append(value)
            return jsonify(test)
        else:
            values = [value for index, value in enumerate(li)]
            return jsonify(values)

@app.route("/detailed", methods=["GET","POST"])
def detailed():
    if request.method == "POST":
        selectedURL = request.form.get("row")
        details = getRow(selectedURL)
        print(details)
        return jsonify(details)
    else:
        return jsonify("Error")

if __name__ == "__main__":
    app.run(host="0.0.0.0")#, debug=True)