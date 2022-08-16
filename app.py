from flask import Flask
from scrapper import getScrappedData

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return "<h1>Hello World!</h1>"

@app.route('/<publicAddress>')
def api(publicAddress):
    return getScrappedData(publicAddress)


if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)