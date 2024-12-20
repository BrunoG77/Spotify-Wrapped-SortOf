from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
# Used UserMixin to use current_user

# Blueprint means there are roots/URLS inside here
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                # login user
                login_user(user, remember=True)
                return redirect(url_for('home.home_page'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist here', category='error')
               
    return render_template('login.html', user=current_user)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('sign-up', methods=['GET', 'POST'])
def sign_up():
    # Get user info with POST
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('fname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        # Check if values are acceptable
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already exists', category='error')
            
        elif len(email) < 5:
            # Use flash library to flash in case of error or success
            flash('Email not valid', category='error')
        
        elif len(fname) <= 2:
            flash('First name must be over 2 characters', category='error')
        
        elif password1 != password2:
            flash('Passwords must be equal', category='error')
        
        elif len(password1) < 5:
            flash('Password must be over 4 characters', category='error')
        
        else:
            # add user to the database
            new_user = User(email = email, f_name = fname, password = generate_password_hash(password1, method='sha256'))
            
            db.session.add(new_user)
            # refresh
            db.session.commit()
            # login user
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('home.home_page'))
        
    
    return render_template('signup.html', user=current_user)