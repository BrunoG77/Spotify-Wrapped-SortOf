from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from flask_login import login_required, logout_user, current_user
from . import db, get_token 
from .models import Wrapped, Artists, Tracks
import spotipy

# Blueprint means there are routes/URLS inside here
wrapped = Blueprint('wrapped', __name__)

@wrapped.route('/wrapped', methods=['GET','POST'])
@login_required
def do_wrapped():
    try:
        token_info = get_token()
    except:
        print('\nUser not logged in\n')
        redirect(url_for("auth.login", _external=False))
    
    # use spotipy to check user
    sp = spotipy.Spotify(auth= token_info['access_token'])
    
    
    # do spotify wrapped
    if request.method == 'POST':
        # get type of wrapped wanted by the user
        type = request.form['wrapped_type']
        
        # get user saved tracks
        top_artists = sp.current_user_top_artists(limit=5, offset=0, time_range=type)['items']
        
        # get user most listened tracks
        top_tracks = sp.current_user_top_tracks(limit=5, offset=0, time_range=type)['items']

        #check if there are any artists and tracks
        if len(top_artists) < 1:
            flash('There are no artists!', category='error')
        elif len(top_tracks) < 1:
            flash('There are no tracks!', category='error')
        else:
            # calculate wrapped
            artists = []
            tracks = []
            
            # Position of podium
            n = 1
            
            for artist in top_artists:
                # get user top 5 artists
                artists.append(str(n) + ' ' + artist['name'])
                n += 1

            # reset n
            n = 1
            
            for track in top_tracks:
                # get user top 5 tracks and respective artist
                tracks.append(str(n) + ' ' + track['name'])
                n += 1
                
            # add wrapped to data
            new_wrapped = Wrapped(type = type, user_id = current_user.id)
            db.session.add(new_wrapped)
            db.session.commit()
            
            # add artists and tracks to database
            if type == 'short_term':
                for artist in artists:
                    new_artist = Artists(short_term = artist, wrapped_id = int(new_wrapped.id))
                    db.session.add(new_artist)
                    db.session.commit()
                
                for track in tracks:
                    new_track = Tracks(short_term = track, wrapped_id = int(new_wrapped.id))
                    db.session.add(new_track)
                    db.session.commit()
                    
            elif type == 'medium_term':
                for artist in artists:
                    new_artist = Artists(medium_term = artist, wrapped_id = int(new_wrapped.id))
                    db.session.add(new_artist)
                    db.session.commit()
                
                for track in tracks:
                    new_track = Tracks(medium_term = track, wrapped_id = int(new_wrapped.id))
                    db.session.add(new_track)
                    db.session.commit()
                    
            elif type == 'long_term':
                for artist in artists:
                    new_artist = Artists(long_term = artist, wrapped_id = int(new_wrapped.id))
                    db.session.add(new_artist)
                    db.session.commit()
                
                for track in tracks:
                    new_track = Tracks(long_term = track, wrapped_id = int(new_wrapped.id))
                    db.session.add(new_track)
                    db.session.commit()
                
            else:
                flash('Wrapped failed', category='error')
            
            flash('Wrapped succesfully concluded!', category='success')
            
            # prepare text
            top5_art = 'Top 5 Artists'
            top5_tra = 'Top 5 Tracks'
            
            return render_template('wrapped.html', user=current_user, artists=artists, tracks=tracks,
                                   top5_art = top5_art, top5_tra = top5_tra)
        
    return render_template('wrapped.html', user=current_user)
