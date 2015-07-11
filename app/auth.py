from flask_httpauth import HTTPBasicAuth
import os

auth = HTTPBasicAuth()

users = {
    os.getenv('username'): os.getenv('password')
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None
