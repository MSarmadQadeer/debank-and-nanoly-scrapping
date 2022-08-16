from flask import Flask

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return "<h1>Hello World!</h1>"


if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)