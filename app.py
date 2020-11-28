from flask import Flask, request, render_template, redirect, flash, jsonify, session, g
from flask_debugtoolbar import DebugToolbarExtension 
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Address, State, get_favs
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


@app.before_request
def add_user_to_g():
    """If logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def user_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


# def do_logout():
#     """Logout user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]


@app.route('/')
def welcome():
    """shows homepage"""
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

        return redirect('/home')

    return render_template('/user/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def user_login():
    form = userLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            user_login(user)
            flash("welcome back!", "success")
            return redirect('/home')
        else:
            flash("Invalid password, try again", "danger")


    return render_template('/user/login.html', form=form)


@app.route('/home')
def show_home_dashboard():
    """shows dashboard with homestate information"""

    if not g.user:
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")


    user = User.query.get_or_404(g.user.id)

    data = get_state_data(user.homestate)


    return render_template('/user/home.html', user=user, data=data)


