from dotenv import load_dotenv
import os
from flask import Flask, redirect, request, session, url_for
import requests
import json
import base64

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")


def main():
    print("Hello world!")

def urlencode(params):
    return "&".join([str(key) + "=" + str(value) for  key, value in params.items()])        

@app.route("/")
def root():
    return redirect(redirect_auth_url())

@app.route("/callback")
def callback():
    code = request.args.get("code")

    auth_str = client_id + ":" + client_secret
    auth_uft8 = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_uft8)

    header = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization" : "Basic " + str(auth_base64, "utf-8")
    }
    payload = {
        "grant_type" : "client_credentials",
        "code" : code,
        "redirect_uri" : url_for("get_top_tracks"),
    }
    response = requests.post("https://accounts.spotify.com/api/token", headers=header, params=payload)
    response_json = json.loads(response.content)

    print(response_json)

    token = response_json["access_token"]
    return {"token" : token}

@app.route("/get_top_tracks")
def get_top_tracks():
    return {"get_top_tokens" : "hello!"}

def redirect_auth_url():
    response_type = "code"
    redirect_uri = "http://127.0.0.1:5000/callback"
    scope = ""

    params = {
        "client_id" : client_id,
        "response_type" : response_type,
        "redirect_uri" : redirect_uri,
        "scope" : scope,
    }

    return "https://accounts.spotify.com/authorize?" + urlencode(params)


if __name__ == "__main__":
    main()