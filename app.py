from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension 
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, State, User, Address, User_Addresses 
from forms import userLoginForm, userSignUpForm

from route_helpers import get_state_data



app = Flask(__name__)

# connect to specific database in postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_draft'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "key9876"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# db.create_all()

CURR_USER_KEY = "current_user"


# Funcs to find and authenticate user via flask session
def find_user():

    if CURR_USER_KEY in session:
        found_user = User.query.get(session[CURR_USER_KEY])
        return found_user

    else:
        return None

def user_login(user):
    session[CURR_USER_KEY] = user.id

def logout_user():
    session[CURR_USER_KEY] = None



@app.route('/')
def welcome():
    """shows homepage for all anon users"""
    return render_template('welcome.html')

@app.route('/signup', methods=["GET", "POST"])
def handle_signup():

    form = userSignUpForm()

    if form.validate_on_submit():
        try:
            new_user = User.signUp(
                username = form.username.data,
                email = form.email.data,
                password = form.password.data,
                homestate = form.homestate.data
            )
            db.session.commit()

        except IntegrityError:
            flash('Username already taken', 'danger')
            return render_template('/user/signup.html', form=form)
        
        user_login(new_user)

        return redirect('/dashboard')

    return render_template('/user/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def user_login_route():
    form = userLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            user_login(user)
            flash("welcome back!", "success")
            return redirect('/dashboard')
        else:
            flash("Invalid password, try again", "danger")


    return render_template('/user/login.html', form=form)


@app.route('/dashboard')
def show_home_dashboard():
    """shows dashboard with homestate information"""

    curr_user = User.query.get(session[CURR_USER_KEY])
    session_user = find_user()

    if (session_user is None):
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")


    data = get_state_data(curr_user.homestate)


    return render_template('/user/dashboard.html', user=curr_user, data=data)

@app.route('/logout')
def handle_user_logout():
    if (find_user()):
        flash("Logged out", "success")
        logout_user()
    return redirect('/')
  