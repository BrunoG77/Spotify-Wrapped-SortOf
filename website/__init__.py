import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import time

# initiate database
db = SQLAlchemy()
DB_NAME = "database.db"

#setup flask server
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'lioa9j39v7 839alv821g'
    app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'
    # Locate database in website
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # initialize database and what to use it with
    db.init_app(app)
    
    # import blueprints to register them
    from .home import home
    from .auth import auth
    from .wrapped import wrapped
    
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(wrapped, url_prefix='/')
    
    from .models import User, Wrapped, Artists, Tracks
    
    create_database(app)
    
    login_manager = LoginManager()
    # define where to go if user not logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # decorator telling to use this function to load user
    @login_manager.user_loader
    def load_user(id):
        try: 
            # .get gets primary key
            return User.query.get(int(id))
        
        except:
            return None
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # Create the database
        db.create_all(app=app)

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = "", #Client ID would be here
        client_secret = "", #Client secret would be here
        redirect_uri = url_for('home.redirectPage', _external=True),
        scope = "user-top-read"
    )
 
def get_token():
    # get token info from the session cookie,
    # if it doenst exist, then return NONE
    token_info = session.get('token_info', None)
    
    # if it is NONE, throw an exception
    if not token_info:
        raise 'exception'
    
    # Get the time
    now = int(time.time())
    
    # check how long until token expires
    expired = token_info['expires_at'] - now
    
    # If its less than 60, refresh it
    if expired < 60:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    
    return token_info
