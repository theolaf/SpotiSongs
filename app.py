from flask import Flask, render_template, request, redirect, url_for, session, make_response
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
scope = ["user-library-read", "user-top-read"]

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET').encode('utf8')

sp_client = spotipy.client.Spotify()

@app.route("/")
def index():
    if "token_info" not in session:
        return render_template("index.html")
    else:
        sp_client.set_auth(session.get('token_info').get('access_token'))
        return "Salut " + sp_client.me()["display_name"] + " ! Ton artiste préféré est " + str(sp_client.current_user_top_artists(limit=1)["items"][0]["name"])

@app.route("/login")
def login():
    auth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
    return redirect(auth.get_authorize_url())

@app.route("/api_callback")
def api_callback():
    auth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
    session.clear()
    code = request.args.get('code')
    if code is not None:
        token_info = auth.get_access_token(code)
        session["token_info"] = token_info

    return redirect(url_for('index'))
