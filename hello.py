from flask import Flask
from views.home import Home

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def hello():
    return Home.render()
