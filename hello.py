from flask import Flask
import views

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def hello():
    return views.Home.render()


@app.route('/list-invites')
def listInvites():
    return views.ListInvites.render()
