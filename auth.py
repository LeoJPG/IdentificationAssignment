#!/bin/python3

from urllib.request import urlopen, Request
from flask import Flask, session, redirect, url_for
from flask_oauthlib.client import OAuth
import base64

website = """PCEg4oCT4oCTIENyZWRpdCB0byBodHRwczovL3d3dy53M3NjaG9vbHMuY29tL2dyYXBoaWNzL2dhbWVfaW50cm8uYXNwIOKAk+KAkz4gCgo8IURPQ1RZUEUgaHRtbD4KPGh0bWw+CjxoZWFkPgo8bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBpbml0aWFsLXNjYWxlPTEuMCIvPgo8c3R5bGU+CmNhbnZhcyB7CiAgICBib3JkZXI6MXB4IHNvbGlkICNkM2QzZDM7CiAgICBiYWNrZ3JvdW5kLWNvbG9yOiAjZjFmMWYxOwp9Cjwvc3R5bGU+CjwvaGVhZD4KPGJvZHkgb25sb2FkPSJzdGFydEdhbWUoKSI+CjxzY3JpcHQ+Cgp2YXIgbXlHYW1lUGllY2U7CnZhciBteU9ic3RhY2xlcyA9IFtdOwp2YXIgbXlTY29yZTsKCmZ1bmN0aW9uIHN0YXJ0R2FtZSgpIHsKICAgIG15R2FtZVBpZWNlID0gbmV3IGNvbXBvbmVudCgzMCwgMzAsICJyZWQiLCAxMCwgMTIwKTsKICAgIG15R2FtZVBpZWNlLmdyYXZpdHkgPSAwLjA1OwogICAgbXlTY29yZSA9IG5ldyBjb21wb25lbnQoIjMwcHgiLCAiQ29uc29sYXMiLCAiYmxhY2siLCAyODAsIDQwLCAidGV4dCIpOwogICAgbXlHYW1lQXJlYS5zdGFydCgpOwp9Cgp2YXIgbXlHYW1lQXJlYSA9IHsKICAgIGNhbnZhcyA6IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoImNhbnZhcyIpLAogICAgc3RhcnQgOiBmdW5jdGlvbigpIHsKICAgICAgICB0aGlzLmNhbnZhcy53aWR0aCA9IDQ4MDsKICAgICAgICB0aGlzLmNhbnZhcy5oZWlnaHQgPSAyNzA7CiAgICAgICAgdGhpcy5jb250ZXh0ID0gdGhpcy5jYW52YXMuZ2V0Q29udGV4dCgiMmQiKTsKICAgICAgICBkb2N1bWVudC5ib2R5Lmluc2VydEJlZm9yZSh0aGlzLmNhbnZhcywgZG9jdW1lbnQuYm9keS5jaGlsZE5vZGVzWzBdKTsKICAgICAgICB0aGlzLmZyYW1lTm8gPSAwOwogICAgICAgIHRoaXMuaW50ZXJ2YWwgPSBzZXRJbnRlcnZhbCh1cGRhdGVHYW1lQXJlYSwgMjApOwogICAgICAgIH0sCiAgICBjbGVhciA6IGZ1bmN0aW9uKCkgewogICAgICAgIHRoaXMuY29udGV4dC5jbGVhclJlY3QoMCwgMCwgdGhpcy5jYW52YXMud2lkdGgsIHRoaXMuY2FudmFzLmhlaWdodCk7CiAgICB9Cn0KCmZ1bmN0aW9uIGNvbXBvbmVudCh3aWR0aCwgaGVpZ2h0LCBjb2xvciwgeCwgeSwgdHlwZSkgewogICAgdGhpcy50eXBlID0gdHlwZTsKICAgIHRoaXMuc2NvcmUgPSAwOwogICAgdGhpcy53aWR0aCA9IHdpZHRoOwogICAgdGhpcy5oZWlnaHQgPSBoZWlnaHQ7CiAgICB0aGlzLnNwZWVkWCA9IDA7CiAgICB0aGlzLnNwZWVkWSA9IDA7ICAgIAogICAgdGhpcy54ID0geDsKICAgIHRoaXMueSA9IHk7CiAgICB0aGlzLmdyYXZpdHkgPSAwOwogICAgdGhpcy5ncmF2aXR5U3BlZWQgPSAwOwogICAgdGhpcy51cGRhdGUgPSBmdW5jdGlvbigpIHsKICAgICAgICBjdHggPSBteUdhbWVBcmVhLmNvbnRleHQ7CiAgICAgICAgaWYgKHRoaXMudHlwZSA9PSAidGV4dCIpIHsKICAgICAgICAgICAgY3R4LmZvbnQgPSB0aGlzLndpZHRoICsgIiAiICsgdGhpcy5oZWlnaHQ7CiAgICAgICAgICAgIGN0eC5maWxsU3R5bGUgPSBjb2xvcjsKICAgICAgICAgICAgY3R4LmZpbGxUZXh0KHRoaXMudGV4dCwgdGhpcy54LCB0aGlzLnkpOwogICAgICAgIH0gZWxzZSB7CiAgICAgICAgICAgIGN0eC5maWxsU3R5bGUgPSBjb2xvcjsKICAgICAgICAgICAgY3R4LmZpbGxSZWN0KHRoaXMueCwgdGhpcy55LCB0aGlzLndpZHRoLCB0aGlzLmhlaWdodCk7CiAgICAgICAgfQogICAgfQogICAgdGhpcy5uZXdQb3MgPSBmdW5jdGlvbigpIHsKICAgICAgICB0aGlzLmdyYXZpdHlTcGVlZCArPSB0aGlzLmdyYXZpdHk7CiAgICAgICAgdGhpcy54ICs9IHRoaXMuc3BlZWRYOwogICAgICAgIHRoaXMueSArPSB0aGlzLnNwZWVkWSArIHRoaXMuZ3Jhdml0eVNwZWVkOwogICAgICAgIHRoaXMuaGl0Qm90dG9tKCk7CiAgICB9CiAgICB0aGlzLmhpdEJvdHRvbSA9IGZ1bmN0aW9uKCkgewogICAgICAgIHZhciByb2NrYm90dG9tID0gbXlHYW1lQXJlYS5jYW52YXMuaGVpZ2h0IC0gdGhpcy5oZWlnaHQ7CiAgICAgICAgaWYgKHRoaXMueSA+IHJvY2tib3R0b20pIHsKICAgICAgICAgICAgdGhpcy55ID0gcm9ja2JvdHRvbTsKICAgICAgICAgICAgdGhpcy5ncmF2aXR5U3BlZWQgPSAwOwogICAgICAgIH0KICAgIH0KICAgIHRoaXMuY3Jhc2hXaXRoID0gZnVuY3Rpb24ob3RoZXJvYmopIHsKICAgICAgICB2YXIgbXlsZWZ0ID0gdGhpcy54OwogICAgICAgIHZhciBteXJpZ2h0ID0gdGhpcy54ICsgKHRoaXMud2lkdGgpOwogICAgICAgIHZhciBteXRvcCA9IHRoaXMueTsKICAgICAgICB2YXIgbXlib3R0b20gPSB0aGlzLnkgKyAodGhpcy5oZWlnaHQpOwogICAgICAgIHZhciBvdGhlcmxlZnQgPSBvdGhlcm9iai54OwogICAgICAgIHZhciBvdGhlcnJpZ2h0ID0gb3RoZXJvYmoueCArIChvdGhlcm9iai53aWR0aCk7CiAgICAgICAgdmFyIG90aGVydG9wID0gb3RoZXJvYmoueTsKICAgICAgICB2YXIgb3RoZXJib3R0b20gPSBvdGhlcm9iai55ICsgKG90aGVyb2JqLmhlaWdodCk7CiAgICAgICAgdmFyIGNyYXNoID0gdHJ1ZTsKICAgICAgICBpZiAoKG15Ym90dG9tIDwgb3RoZXJ0b3ApIHx8IChteXRvcCA+IG90aGVyYm90dG9tKSB8fCAobXlyaWdodCA8IG90aGVybGVmdCkgfHwgKG15bGVmdCA+IG90aGVycmlnaHQpKSB7CiAgICAgICAgICAgIGNyYXNoID0gZmFsc2U7CiAgICAgICAgfQogICAgICAgIHJldHVybiBjcmFzaDsKICAgIH0KfQoKZnVuY3Rpb24gdXBkYXRlR2FtZUFyZWEoKSB7CiAgICB2YXIgeCwgaGVpZ2h0LCBnYXAsIG1pbkhlaWdodCwgbWF4SGVpZ2h0LCBtaW5HYXAsIG1heEdhcDsKICAgIGZvciAoaSA9IDA7IGkgPCBteU9ic3RhY2xlcy5sZW5ndGg7IGkgKz0gMSkgewogICAgICAgIGlmIChteUdhbWVQaWVjZS5jcmFzaFdpdGgobXlPYnN0YWNsZXNbaV0pKSB7CiAgICAgICAgICAgIHJldHVybjsKICAgICAgICB9IAogICAgfQogICAgbXlHYW1lQXJlYS5jbGVhcigpOwogICAgbXlHYW1lQXJlYS5mcmFtZU5vICs9IDE7CiAgICBpZiAobXlHYW1lQXJlYS5mcmFtZU5vID09IDEgfHwgZXZlcnlpbnRlcnZhbCgxNTApKSB7CiAgICAgICAgeCA9IG15R2FtZUFyZWEuY2FudmFzLndpZHRoOwogICAgICAgIG1pbkhlaWdodCA9IDIwOwogICAgICAgIG1heEhlaWdodCA9IDIwMDsKICAgICAgICBoZWlnaHQgPSBNYXRoLmZsb29yKE1hdGgucmFuZG9tKCkqKG1heEhlaWdodC1taW5IZWlnaHQrMSkrbWluSGVpZ2h0KTsKICAgICAgICBtaW5HYXAgPSA1MDsKICAgICAgICBtYXhHYXAgPSAyMDA7CiAgICAgICAgZ2FwID0gTWF0aC5mbG9vcihNYXRoLnJhbmRvbSgpKihtYXhHYXAtbWluR2FwKzEpK21pbkdhcCk7CiAgICAgICAgbXlPYnN0YWNsZXMucHVzaChuZXcgY29tcG9uZW50KDEwLCBoZWlnaHQsICJncmVlbiIsIHgsIDApKTsKICAgICAgICBteU9ic3RhY2xlcy5wdXNoKG5ldyBjb21wb25lbnQoMTAsIHggLSBoZWlnaHQgLSBnYXAsICJncmVlbiIsIHgsIGhlaWdodCArIGdhcCkpOwogICAgfQogICAgZm9yIChpID0gMDsgaSA8IG15T2JzdGFjbGVzLmxlbmd0aDsgaSArPSAxKSB7CiAgICAgICAgbXlPYnN0YWNsZXNbaV0ueCArPSAtMTsKICAgICAgICBteU9ic3RhY2xlc1tpXS51cGRhdGUoKTsKICAgIH0KICAgIG15U2NvcmUudGV4dD0iU0NPUkU6ICIgKyBteUdhbWVBcmVhLmZyYW1lTm87CiAgICBteVNjb3JlLnVwZGF0ZSgpOwogICAgbXlHYW1lUGllY2UubmV3UG9zKCk7CiAgICBteUdhbWVQaWVjZS51cGRhdGUoKTsKfQoKZnVuY3Rpb24gZXZlcnlpbnRlcnZhbChuKSB7CiAgICBpZiAoKG15R2FtZUFyZWEuZnJhbWVObyAvIG4pICUgMSA9PSAwKSB7cmV0dXJuIHRydWU7fQogICAgcmV0dXJuIGZhbHNlOwp9CgpmdW5jdGlvbiBhY2NlbGVyYXRlKG4pIHsKICAgIG15R2FtZVBpZWNlLmdyYXZpdHkgPSBuOwp9Cjwvc2NyaXB0Pgo8YnI+CjxidXR0b24gb25tb3VzZWRvd249ImFjY2VsZXJhdGUoLTAuMikiIG9ubW91c2V1cD0iYWNjZWxlcmF0ZSgwLjA1KSI+QUNDRUxFUkFURTwvYnV0dG9uPgo8cD5Db25ncmF0dWxhdGlvbnMsIHlvdSd2ZSBhY2Nlc3NlZCB0aGUgZ2FtZSE8L3A+CjxwPkhvdyBsb25nIGNhbiB5b3Ugc3RheSBhbGl2ZT88L3A+CjwvYm9keT4KPC9odG1sPgo="""



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
                          request_token_params={'scope': 'openid profile email'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          consumer_key=GOOGLE_ID,
                          consumer_secret=GOOGLE_SECRET)


@app.route("/")
def index():
    token = session.get("access_token")
    id_token = session.get("id_token")
    print("This is your access token: " + str(token))
    print("And this is your ID token: " + str(id_token))
    if token is None:
        return redirect(url_for("login"))
    headers = {'Authorization' : 'OAuth ' + token[0]}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)

    res = urlopen(req)
    user_name = res.read().decode("utf-8").split('name": "')[1].split('",')[0]
    print(user_name)
    return ("<h1>Hello there " + str(user_name) + " :3 </h1>").encode("utf-8") + base64.b64decode(website)

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
    id_token = resp["id_token"]
    session['access_token'] = token, ''
    session["id_token"] = id_token, ""
    return redirect(url_for('index'))

@google.tokengetter
def get_access_token():
    return session.get('access_token')

@google.tokengetter
def get_id_token():
    return session.get("id_token")

if __name__ == ("__main__"):
    app.run(host="127.0.0.1", port=8000)
