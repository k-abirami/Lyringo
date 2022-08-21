from flask import Flask, render_template, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time, json

app = Flask(__name__)

app.secret_key = "ONcs92894fhno"
app.config['SESSION_COOKIE_NAME'] = 'Lyringo Cookie'
TOKEN_INFO = "token_info"

with open('config.json') as config_file:
    config_data = json.load(config_file)

@app.route("/")
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external = True))

@app.route("/getTracks")
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external = False))
    sp = spotipy.Spotify(auth=token_info['access_token'])

    return sp.current_user_saved_tracks(limit=50, offset = 0)

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"

    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(       
        client_id=config_data['id'],
        client_secret=config_data['secret'],
        redirect_uri=url_for('redirectPage', _external = True),
        scope = "user-library-read")
    

@app.route("/home")
def home():
 return render_template("index.html")

@app.route("/about")
def about():
 return render_template("about.html")

@app.route("/flashcards")
def flashcard():
 return render_template("flashcards.html")

@app.route("/signin")
def signin():
 return render_template("signin.html")

@app.route("/signup")
def signup():
 return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)