from flask import Flask, render_template
from scrapper import getScrappedData

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html", title="Home Screen")


@app.route('/<publicAddress>')
def apiCall(publicAddress):
    results = getScrappedData(publicAddress)
    return render_template("index.html", title="Results Screen", results=results)


if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)
