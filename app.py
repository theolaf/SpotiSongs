from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import uuid

###### GETTING ENV VARS ######
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
scope = ["user-library-read", "user-top-read"]

###### CREATING THE FLASK APP AND SPOTIPY CLIENT ######
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET').encode('utf8')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')

###### HOME ######
@app.route("/")
def index():
    if not session.get('uuid'): # if visitor unknown create a new id
        session.permanent = False
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, cache_handler=cache_handler)

    if request.args.get("code"): # if redirected from spotify login
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()): # render login when no token found
        return render_template("login.html", auth_url=auth_manager.get_authorize_url())

    try:
        sp_client = spotipy.Spotify(auth_manager=auth_manager)
        name = sp_client.me()["display_name"] # get user's name
        print(name)
        top_tracks = [track["id"] for track in sp_client.current_user_top_tracks(limit=10)["items"]] # get user's top 10 tracks
        last_saves = [track["track"]["id"] for track in sp_client.current_user_saved_tracks(limit=10)["items"]] # get user's last 10 saved tracks
        return render_template("home.html", name=name, top_tracks=top_tracks, last_saves=last_saves)

    except spotipy.exceptions.SpotifyException as e: # if the token has expired, the user has to reconnect
        return render_template("login.html", auth_url=auth_manager.get_authorize_url())

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
