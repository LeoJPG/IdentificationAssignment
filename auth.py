#!/bin/python3

import hashlib
from flask import Flask, session, redirect, url_for
from flask_oauthlib.client import OAuth

api_key = "AIzaSyCFbc3ww8ww1loun6n9vv-wawXKImY4ByQ"

GOOGLE_ID = "109537785519-cqngec7i924b6ojtvj8mm99urk9gvpup.apps.googleusercontent.com"
GOOGLE_SECRET = "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"
SECRET_KEY = "gGfdsD&3Z9za"

REDIRECT_URI = "/authorized"


app = Flask(__name__)
app.secret_key = SECRET_KEY
oauth = OAuth()

google = oauth.remote_app("google",
                          base_url="https://accounts.google.com",
                          authorize_url="https://accounts.google.com/o/oauth2/auth",
                          request_token_url=None,
                          request_token_params={'scope': 'openid email'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          consumer_key=GOOGLE_ID,
                          consumer_secret=GOOGLE_SECRET)


@app.route("/")
def index():
    token = session.get("access_token")
    print("This is your token: " + str(token))
    if token is None:
        return redirect(url_for("login"))
    return "<p>:C</p>"

@app.route("/login")
def login():
    print("You are logged in! congrats!")
    yeyorney = google.authorize(callback=url_for("authorized", _external=True))
    print(yeyorney)
    print(session.get("access_token"))
    return google.authorize(callback=url_for("authorized", _external=True))

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    token = resp['access_token']
    session['access_token'] = token, ''
    return redirect(url_for('index'))

@google.tokengetter
def get_access_token():
    return session.get('access_token')

if __name__ == ("__main__"):
    app.run(host="127.0.0.1", port=8000)
