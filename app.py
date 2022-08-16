from unittest import result
from flask import Flask, render_template
from scrapper import getScrappedData

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html", title="Hello")


@app.route('/<publicAddress>')
def apiCall(publicAddress):
    results = getScrappedData(publicAddress)
    return render_template("index.html", title="API Call", results=results)


if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)
