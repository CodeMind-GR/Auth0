import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

streamlit_app_url = env.get("STREAMLIT_APP_URL")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    userinfo_endpoint = f"https://{env.get('AUTH0_DOMAIN')}/userinfo"
    resp = oauth.auth0.get(userinfo_endpoint)
    userinfo = resp.json()
    email = userinfo.get('email')
    name = userinfo.get('name')

    session["user"] = userinfo

    return redirect(f"{streamlit_app_url}/?token={token['access_token']}&email={quote_plus(email)}&name={quote_plus(name)}")


@app.route("/logout")
def logout():
    session.clear()
    # 로그아웃 후 Streamlit 앱으로 리디렉션합니다.
    return redirect(f"{streamlit_app_url}/?logout=True")


@app.route("/")
def home():
    # 홈 라우트 접근 시 Streamlit 앱의 홈으로 리디렉션합니다.
    return redirect(streamlit_app_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))