from flask import Flask, render_template, request, redirect, url_for, session, make_response
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

###### GETTING ENV VARS ######
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
scope = ["user-library-read", "user-top-read"]

###### CREATING THE FLASK APP AND SPOTIPY CLIENT ######
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET').encode('utf8')
sp_client = spotipy.client.Spotify()

###### HOME ######
@app.route("/")
def index():
    if "token_info" not in session: #if no token is available in the flask session, show login page
        return render_template("login.html")
    else: #if a token is available in the flask session, show home page
        sp_client.set_auth(session.get('token_info').get('access_token'))
        return "Salut " + sp_client.me()["display_name"] + " ! Ton artiste préféré est " + str(sp_client.current_user_top_artists(limit=1)["items"][0]["name"])

###### AUTH PROTOCOL ######
@app.route("/login")
def login():
    auth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
    return redirect(auth.get_authorize_url()) #redirect to the spotify auth page

@app.route("/api_callback")
def api_callback(): #once the user has logged in, the app has to get the associated token and store it in the flask session
    auth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
    session.clear()
    code = request.args.get('code') #get the code sent with the api callback
    if code is not None:
        token_info = auth.get_access_token(code) #get the token corresponding to the code sent by spotify
        session["token_info"] = token_info #store the token in the flask session
    return redirect(url_for('index')) #redirect to the home page

if __name__ == "__main__":
    app.run()
