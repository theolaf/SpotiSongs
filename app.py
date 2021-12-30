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
    callback_code = request.args.get("code")

    if callback_code: # if redirected from spotify login
        auth_manager.get_access_token(callback_code)
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()): # render login page when no token found
        return render_template("login.html", auth_url=auth_manager.get_authorize_url())

    try:
        sp_client = spotipy.Spotify(auth_manager=auth_manager)
        name = sp_client.me()["display_name"] # get user's name
        print(name)
        top_tracks = [track["id"] for track in sp_client.current_user_top_tracks(limit=10)["items"]] # get user's top 10 tracks
        last_saves = [track["track"]["id"] for track in sp_client.current_user_saved_tracks(limit=10)["items"]] # get user's last 10 saved tracks
        return render_template("home.html", name=name, top_tracks=top_tracks, last_saves=last_saves)

    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 403: #if the user isn't registered (Spotify API limitation)
            return render_template("user_not_registered.html")
        else: # for any other http status (401 for example if the token has timed out) simply redirect to login page
            return render_template("login.html", auth_url=auth_manager.get_authorize_url())

@app.route('/signout')
def signout():
    try:
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
