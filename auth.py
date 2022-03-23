#!/bin/python3

from urllib.request import urlopen, Request
from flask import Flask, session, redirect, url_for
from flask_oauthlib.client import OAuth
import base64

website = "PCEgw6LigqzigJzDouKCrOKAnCBDcmVkaXQgdG8gaHR0cHM6Ly93d3cudzNzY2hvb2xzLmNvbS9ncmFwaGljcy9nYW1lX2ludHJvLmFzcCDDouKCrOKAnMOi4oKs4oCcPgoKPCFET0NUWVBFIGh0bWw+CjxodG1sPgo8aGVhZD4KPG1ldGEgbmFtZT0idmlld3BvcnQiIGNvbnRlbnQ9IndpZHRoPWRldmljZS13aWR0aCwgaW5pdGlhbC1zY2FsZT0xLjAiLz4KPG1ldGEgaHR0cC1lcXVpdj0iQ29udGVudC1TZWN1cml0eS1Qb2xpY3kiIGNvbnRlbnQ9IgpkZWZhdWx0LXNyYwogICdzZWxmJwogIGRhdGE6CiAgaHR0cHM6CiAgaHR0cDoKICB3c3M6CiAgJ3Vuc2FmZS1ldmFsJwogICd1bnNhZmUtaW5saW5lJzsKc3R5bGUtc3JjCiAgJ3NlbGYnCiAgJ3Vuc2FmZS1pbmxpbmUnOwptZWRpYS1zcmMgKjsKaW1nLXNyYwogICdzZWxmJwogIGh0dHBzOgpkYXRhOgpjb250ZW50OjsiPgo8c3R5bGU+CmNhbnZhcyB7CiAgICBib3JkZXI6MXB4IHNvbGlkICNkM2QzZDM7CiAgICBiYWNrZ3JvdW5kLWNvbG9yOiAjY2NlNmZmOwp9Cjwvc3R5bGU+CjwvaGVhZD4KPGJvZHkgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6I2Y5YTNhYzsKICAgICAgICAgICAgIGJhY2tncm91bmQtaW1hZ2U6dXJsKCdodHRwczovL3d3dy53YWxscGFwZXJraXNzLmNvbS93aW1nL2IvMTU3LTE1NzMyODBfYmlnLmpwZycpOwogICAgICAgICAgICAgYmFja2dyb3VuZC1yZXBlYXQ6IG5vLXJlcGVhdDsKICAgICAgICAgICAgIGJhY2tncm91bmQtc2l6ZTogODAlOwogICAgICAgICAgICAgYmFja2dyb3VuZC1wb3NpdGlvbjogcmlnaHQgdG9wIj4KPHNjcmlwdD4KCnZhciBteUdhbWVQaWVjZTsKdmFyIG15T2JzdGFjbGVzID0gW107CnZhciBteVNjb3JlOwoKZnVuY3Rpb24gc3RhcnRHYW1lKCkgewogICAgbXlHYW1lUGllY2UgPSBuZXcgY29tcG9uZW50KDMwLCAzMCwgIiNmZjY2Y2MiLCAxMCwgMTIwKTsKICAgIG15R2FtZVBpZWNlLmdyYXZpdHkgPSAwLjA1OwogICAgbXlHYW1lUGllY2Uuc3BlZWRYCiAgICBteVNjb3JlID0gbmV3IGNvbXBvbmVudCgiMzBweCIsICJDb25zb2xhcyIsICJibGFjayIsIDI4MCwgNDAsICJ0ZXh0Iik7CiAgICBteU9ic3RhY2xlcyA9IFtdCiAgICBteUdhbWVBcmVhLnN0YXJ0KCk7Cn0KCnZhciBteUdhbWVBcmVhID0gewogICAgY2FudmFzIDogZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgiY2FudmFzIiksCiAgICBzdGFydCA6IGZ1bmN0aW9uKCkgewogICAgICAgIHRoaXMuY2FudmFzLndpZHRoID0gNDgwOwogICAgICAgIHRoaXMuY2FudmFzLmhlaWdodCA9IDI3MDsKICAgICAgICB0aGlzLmNvbnRleHQgPSB0aGlzLmNhbnZhcy5nZXRDb250ZXh0KCIyZCIpOwogICAgICAgIGRvY3VtZW50LmJvZHkuaW5zZXJ0QmVmb3JlKHRoaXMuY2FudmFzLCBkb2N1bWVudC5ib2R5LmNoaWxkTm9kZXNbMF0pOwogICAgICAgIHRoaXMuZnJhbWVObyA9IDA7CiAgICAgICAgdGhpcy5pbnRlcnZhbCA9IHNldEludGVydmFsKHVwZGF0ZUdhbWVBcmVhLCAyMCk7CiAgICAgICAgfSwKICAgIGNsZWFyIDogZnVuY3Rpb24oKSB7CiAgICAgICAgdGhpcy5jb250ZXh0LmNsZWFyUmVjdCgwLCAwLCB0aGlzLmNhbnZhcy53aWR0aCwgdGhpcy5jYW52YXMuaGVpZ2h0KTsKICAgIH0KfQoKZnVuY3Rpb24gY29tcG9uZW50KHdpZHRoLCBoZWlnaHQsIGNvbG9yLCB4LCB5LCB0eXBlKSB7CiAgICB0aGlzLnR5cGUgPSB0eXBlOwogICAgdGhpcy5zY29yZSA9IDA7CiAgICB0aGlzLndpZHRoID0gd2lkdGg7CiAgICB0aGlzLmhlaWdodCA9IGhlaWdodDsKICAgIHRoaXMuc3BlZWRYID0gMDsKICAgIHRoaXMuc3BlZWRZID0gMDsKICAgIHRoaXMueCA9IHg7CiAgICB0aGlzLnkgPSB5OwogICAgdGhpcy5ncmF2aXR5ID0gMDsKICAgIHRoaXMuZ3Jhdml0eVNwZWVkID0gMDsKICAgIHRoaXMudXBkYXRlID0gZnVuY3Rpb24oKSB7CiAgICAgICAgY3R4ID0gbXlHYW1lQXJlYS5jb250ZXh0OwogICAgICAgIGlmICh0aGlzLnR5cGUgPT0gInRleHQiKSB7CiAgICAgICAgICAgIGN0eC5mb250ID0gdGhpcy53aWR0aCArICIgIiArIHRoaXMuaGVpZ2h0OwogICAgICAgICAgICBjdHguZmlsbFN0eWxlID0gY29sb3I7CiAgICAgICAgICAgIGN0eC5maWxsVGV4dCh0aGlzLnRleHQsIHRoaXMueCwgdGhpcy55KTsKICAgICAgICB9IGVsc2UgewogICAgICAgICAgICBjdHguZmlsbFN0eWxlID0gY29sb3I7CiAgICAgICAgICAgIGN0eC5maWxsUmVjdCh0aGlzLngsIHRoaXMueSwgdGhpcy53aWR0aCwgdGhpcy5oZWlnaHQpOwogICAgICAgIH0KICAgIH0KICAgIHRoaXMubmV3UG9zID0gZnVuY3Rpb24oKSB7CiAgICAgICAgdGhpcy5ncmF2aXR5U3BlZWQgKz0gdGhpcy5ncmF2aXR5OwogICAgICAgIHRoaXMueCArPSB0aGlzLnNwZWVkWDsKICAgICAgICB0aGlzLnkgKz0gdGhpcy5zcGVlZFkgKyB0aGlzLmdyYXZpdHlTcGVlZDsKICAgICAgICB0aGlzLmhpdEJvdHRvbSgpOwogICAgfQogICAgdGhpcy5oaXRCb3R0b20gPSBmdW5jdGlvbigpIHsKICAgICAgICB2YXIgcm9ja2JvdHRvbSA9IG15R2FtZUFyZWEuY2FudmFzLmhlaWdodCAtIHRoaXMuaGVpZ2h0OwogICAgICAgIGlmICh0aGlzLnkgPiByb2NrYm90dG9tKSB7CiAgICAgICAgICAgIHRoaXMueSA9IHJvY2tib3R0b207CiAgICAgICAgICAgIHRoaXMuZ3Jhdml0eVNwZWVkID0gMDsKICAgICAgICB9CiAgICB9CiAgICB0aGlzLmNyYXNoV2l0aCA9IGZ1bmN0aW9uKG90aGVyb2JqKSB7CiAgICAgICAgdmFyIG15bGVmdCA9IHRoaXMueDsKICAgICAgICB2YXIgbXlyaWdodCA9IHRoaXMueCArICh0aGlzLndpZHRoKTsKICAgICAgICB2YXIgbXl0b3AgPSB0aGlzLnk7CiAgICAgICAgdmFyIG15Ym90dG9tID0gdGhpcy55ICsgKHRoaXMuaGVpZ2h0KTsKICAgICAgICB2YXIgb3RoZXJsZWZ0ID0gb3RoZXJvYmoueDsKICAgICAgICB2YXIgb3RoZXJyaWdodCA9IG90aGVyb2JqLnggKyAob3RoZXJvYmoud2lkdGgpOwogICAgICAgIHZhciBvdGhlcnRvcCA9IG90aGVyb2JqLnk7CiAgICAgICAgdmFyIG90aGVyYm90dG9tID0gb3RoZXJvYmoueSArIChvdGhlcm9iai5oZWlnaHQpOwogICAgICAgIHZhciBjcmFzaCA9IHRydWU7CiAgICAgICAgaWYgKChteWJvdHRvbSA8IG90aGVydG9wKSB8fCAobXl0b3AgPiBvdGhlcmJvdHRvbSkgfHwgKG15cmlnaHQgPCBvdGhlcmxlZnQpIHx8IChteWxlZnQgPiBvdGhlcnJpZ2h0KSkgewogICAgICAgICAgICBjcmFzaCA9IGZhbHNlOwogICAgICAgIH0KICAgICAgICByZXR1cm4gY3Jhc2g7CiAgICB9Cn0KCmZ1bmN0aW9uIHVwZGF0ZUdhbWVBcmVhKCkgewogICAgdmFyIHgsIGhlaWdodCwgZ2FwLCBtaW5IZWlnaHQsIG1heEhlaWdodCwgbWluR2FwLCBtYXhHYXA7CiAgICBmb3IgKGkgPSAwOyBpIDwgbXlPYnN0YWNsZXMubGVuZ3RoOyBpICs9IDEpIHsKICAgICAgICBpZiAobXlHYW1lUGllY2UuY3Jhc2hXaXRoKG15T2JzdGFjbGVzW2ldKSkgewogICAgICAgICAgICByZXR1cm47CiAgICAgICAgfQogICAgfQogICAgbXlHYW1lQXJlYS5jbGVhcigpOwogICAgbXlHYW1lQXJlYS5mcmFtZU5vICs9IDE7CiAgICBpZiAobXlHYW1lQXJlYS5mcmFtZU5vID09IDEgfHwgZXZlcnlpbnRlcnZhbCgxNTApKSB7CiAgICAgICAgeCA9IG15R2FtZUFyZWEuY2FudmFzLndpZHRoOwogICAgICAgIG1pbkhlaWdodCA9IDIwOwogICAgICAgIG1heEhlaWdodCA9IDIwMDsKICAgICAgICBoZWlnaHQgPSBNYXRoLmZsb29yKE1hdGgucmFuZG9tKCkqKG1heEhlaWdodC1taW5IZWlnaHQrMSkrbWluSGVpZ2h0KTsKICAgICAgICBtaW5HYXAgPSA1MDsKICAgICAgICBtYXhHYXAgPSAyMDA7CiAgICAgICAgZ2FwID0gTWF0aC5mbG9vcihNYXRoLnJhbmRvbSgpKihtYXhHYXAtbWluR2FwKzEpK21pbkdhcCk7CiAgICAgICAgbXlPYnN0YWNsZXMucHVzaChuZXcgY29tcG9uZW50KDEwLCBoZWlnaHQsICIjYWQzM2ZmIiwgeCwgMCkpOwogICAgICAgIG15T2JzdGFjbGVzLnB1c2gobmV3IGNvbXBvbmVudCgxMCwgeCAtIGhlaWdodCAtIGdhcCwgIiNhZDMzZmYiLCB4LCBoZWlnaHQgKyBnYXApKTsKICAgIH0KICAgIGZvciAoaSA9IDA7IGkgPCBteU9ic3RhY2xlcy5sZW5ndGg7IGkgKz0gMSkgewogICAgICAgIG15T2JzdGFjbGVzW2ldLnggKz0gLTE7CiAgICAgICAgbXlPYnN0YWNsZXNbaV0udXBkYXRlKCk7CiAgICB9CiAgICBteVNjb3JlLnRleHQ9IlNDT1JFOiAiICsgbXlHYW1lQXJlYS5mcmFtZU5vOwogICAgbXlTY29yZS51cGRhdGUoKTsKICAgIG15R2FtZVBpZWNlLm5ld1BvcygpOwogICAgbXlHYW1lUGllY2UudXBkYXRlKCk7Cn0KCmZ1bmN0aW9uIGV2ZXJ5aW50ZXJ2YWwobikgewogICAgaWYgKChteUdhbWVBcmVhLmZyYW1lTm8gLyBuKSAlIDEgPT0gMCkge3JldHVybiB0cnVlO30KICAgIHJldHVybiBmYWxzZTsKfQoKZnVuY3Rpb24gYWNjZWxlcmF0ZShuKSB7CiAgICBteUdhbWVQaWVjZS5ncmF2aXR5ID0gbjsKfQo8L3NjcmlwdD4KPGJyPgo8YnV0dG9uIG9ubW91c2Vkb3duPSJhY2NlbGVyYXRlKC0wLjIpIiBvbm1vdXNldXA9ImFjY2VsZXJhdGUoMC4wNSkiPkFDQ0VMRVJBVEU8L2J1dHRvbj4KPGJ1dHRvbiB0eXBlPSJidXR0b24iIG5hbWU9InN0YXJ0X2J1dHRvbiIgb25jbGljaz0ic3RhcnRHYW1lKCkiPlNUQVJUPC9idXR0b24+CjxwPkNvbmdyYXR1bGF0aW9ucywgeW91J3ZlIGFjY2Vzc2VkIHRoZSBnYW1lITwvcD4KPHA+SG93IGxvbmcgY2FuIHlvdSBzdGF5IGFsaXZlPzwvcD4KPC9ib2R5Pgo8L2h0bWw+Cg=="

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
    #print("This is your access token: " + str(token)) #Debugging info
    #print("And this is your ID token: " + str(id_token)) #Debugging info
    if token is None:
        return redirect(url_for("login"))
    headers = {'Authorization' : 'OAuth ' + token[0]}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)
    try:
        res = urlopen(req)
        res_code = res.getcode()
        #print("Response code: " + str(res_code)) #Debugging info
        user_name = res.read().decode("utf-8").split('name": "')[1].split('",')[0]
        #print(user_name) #Debugging info
        return ("<h1>Hello there " + str(user_name) + " :3 </h1>").encode("utf-8") + base64.b64decode(website)
    except:
        return redirect("login")

@app.route("/login")
def login():
    yeyorney = google.authorize(callback=url_for("authorized", _external=True))
    #print(session.get("access_token")) #Debugging info
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
