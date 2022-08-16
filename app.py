from flask import Flask, render_template
from scrapper import getScrappedData

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html", title="Hello")


@app.route('/<publicAddress>')
def api(publicAddress):
    return getScrappedData(publicAddress)


if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)
