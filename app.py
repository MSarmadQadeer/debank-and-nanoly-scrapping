from flask import Flask
from logging import FileHandler, WARNING
app = Flask(__name__)

file_handler = FileHandler('error.log')
file_handler.setLevel(WARNING)
app.logger.addHandler(file_handler)

try:
    from controllers import *
except Exception as e:
    print(e)