from flask import Flask

app = Flask(__name__)
app.secret_key = 'flask'

from app.controllers import default


