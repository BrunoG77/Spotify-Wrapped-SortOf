from flask import Blueprint, redirect, render_template, request, flash, jsonify, session
from flask_login import login_required, logout_user, current_user
from . import db, create_spotify_oauth
from .models import Wrapped, Artists, Tracks
import json

# Blueprint means there are routes/URLS inside here
home = Blueprint('home', __name__)


@home.route('/')
@login_required
def home_page():
    return render_template('home.html', user=current_user)


@home.route('/spot-auth', methods = ['GET', 'POST'])
@login_required
def spot_login():
    spot_oauth = create_spotify_oauth()
    auth_url = spot_oauth.get_authorize_url()
    return redirect(auth_url)


@home.route('/redirect')
@login_required
def redirectPage():
    # get another oauth object
    # must get it every time
    spot_oauth = create_spotify_oauth()
    #clear any other states
    session.clear()
    # get the authorization code
    code = request.args.get('code')
    # swap the authorization code with an access token with spotify
    token_info = spot_oauth.get_access_token(code)
    # save token information in the session, in the cookie
    session["token_info"] = token_info
    return render_template('redirect.html', user=current_user)


@home.route('/delete-wrapped', methods=['POST'])
def delete_wrapped():
    # takes Json data from post request and load it as a
    # python dictionary
    wrapped = json.loads(request.data)
    
    # access wrappedId from index.js
    wrappedId = wrapped['wrappedId']
    
    # look for wrapped with that id
    wrapped = Wrapped.query.get(wrappedId)
    
    # check if it exists
    if wrapped:
        # if the user has this wrapped
        if wrapped.user_id == current_user.id:
            # delete artists and tracks corresponding rows
            while Artists.query.filter(Artists.wrapped_id == int(wrappedId)).first():
                artist = Artists.query.filter(Artists.wrapped_id == int(wrappedId)).first()
                db.session.delete(artist)
                db.session.commit()
                
            while Tracks.query.filter(Tracks.wrapped_id == int(wrappedId)).first():
                track = Tracks.query.filter(Tracks.wrapped_id == int(wrappedId)).first()
                db.session.delete(track)
                db.session.commit()

            # delete the wrapped
            db.session.delete(wrapped)
            db.session.commit()
            
    # return an empty response
    return jsonify({})