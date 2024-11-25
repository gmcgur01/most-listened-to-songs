from dotenv import load_dotenv
import os
from fastapi import FastAPI
import uvicorn
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = FastAPI()

@app.get("/")
def main():
    return redirect_auth_url()

@app.get("/redirect")
def redirect(code: str = "", state: str = ""):
    return {"code" : code}

def redirect_auth_url():
    response_type = "code"
    redirect_uri = "http://127.0.0.1:3000/redirect"
    scope = ""

    params = {
        "client_id" : client_id,
        "response_type" : response_type,
        "redirect_uri" : redirect_uri,
        "scope" : scope,
    }

    return RedirectResponse("https://accounts.spotify.com/authorize?" + urlencode(params))


if __name__ == "__main__":
    uvicorn.run("main:app", port=3000, log_level="info")