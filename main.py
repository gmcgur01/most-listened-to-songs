from dotenv import load_dotenv
import os
from flask import Flask, redirect, request, session, url_for
import requests
import json
import base64
import time

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")


def main():
    print("Hello world!")

def urlencode(params):
    return "&".join([str(key) + "=" + str(value).replace(" ", "%20") for  key, value in params.items()])        

@app.route("/")
def root():
    session.clear()
    return redirect(redirect_auth_url())

@app.route("/callback")
def callback():
    code = request.args.get("code")
    session["code"] = code
    return redirect(url_for("get_top_tracks"))

    # return redirect(url_for("get_top_tracks"))

@app.route("/get_top_tracks")
def get_top_tracks():
    token = get_token()
    if token == None:
        return redirect(redirect_auth_url())
    
    header = {
        "Authorization" : f"Bearer {token}"
    }
    params = {
        "time_range" : "long_term",
        "limit" : 50,
    }
    url = "https://api.spotify.com/v1/me/top/tracks?" + urlencode(params)

    response = requests.get(url, headers=header)
    response_json = json.loads(response.content)

    items = response_json["items"]

    top_tracks = [item["name"] for item in items]

    print(top_tracks)

    return response_json

def redirect_auth_url():
    response_type = "code"
    redirect_uri = "http://127.0.0.1:5000/callback"
    scope = "user-read-private user-read-email user-top-read"

    params = {
        "client_id" : client_id,
        "response_type" : response_type,
        "redirect_uri" : redirect_uri,
        "scope" : scope,
        "show_dialog" : "true",
    }

    return "https://accounts.spotify.com/authorize?" + urlencode(params)


def get_token():
    if "code" not in session:
        print("Code not found in the session data!")
        return None
    
    if "token" in session:
        token, expiration_time = session["token"]
        if (expiration_time > int(time.time())):
            print("Token found in session data!")
            return token
        
    print("Requesting a new token!")

    code = session["code"]

    auth_str = client_id + ":" + client_secret
    auth_uft8 = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_uft8)

    header = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization" : "Basic " + str(auth_base64, "utf-8")
    }
    payload = {
        "grant_type" : "authorization_code",
        "code" : code,
        "redirect_uri" : "http://127.0.0.1:5000/callback",
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=header, params=payload)
    response_json = json.loads(response.content)

    token = response_json["access_token"]
    expires_in = int(response_json["expires_in"])
    expiration_time = expires_in + int(time.time())
    session["token"] = (token, expiration_time)

    return token

if __name__ == "__main__":
    app.run()