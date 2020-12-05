from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_mail import Mail, Message
from flask_debugtoolbar import DebugToolbarExtension 
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, State, User, Address, User_Addresses, get_favs 
from forms import userLoginForm, userSignUpForm, addFavoriteForm, editUserForm

from route_helpers import get_state_data, get_multi_state_data
from extra import my_password



app = Flask(__name__)



app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'becky.schmitthenner@gmail.com',
    MAIL_PASSWORD = my_password,
))
mail = Mail(app)


# connect to specific database in postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_draft2'
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

# ******************************************************************** USER ROUTES

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

@app.route('/user/<int:user_id>/edit', methods=["GET", "POST"])
def handle_edit_user(user_id):
    form = editUserForm()
    user = User.query.get(user_id)

    if form.validate_on_submit():
        email = form.email.data
        homestate = form.homestate.email

        user.email = email
        user.homestate = homestate
        db.session.commit()

        return redirect('user/profile')
        # need to create profile page? or dash

    return render_template('/user/edit.html', form=form)
        # create edit form



@app.route('/logout')
def handle_user_logout():
    if (find_user()):
        flash("Logged out", "success")
        logout_user()
    return redirect('/')
  

# ******************************************************************** FAVORITE ROUTES
@app.route('/favorite/add', methods=["GET", "POST"])
def handle_add_favorite_form():

    curr_user = User.query.get(session[CURR_USER_KEY])
    session_user = find_user()

    if (session_user is None):
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")

    form = addFavoriteForm()

    if form.validate_on_submit():

        try: 
            new_fav = Address(
                user_id = curr_user.id,
                address_line1 = form.address_line1.data,
                address_line2 = form.address_line2.data or None,
                state_name = form.state_name.data,
                zip_code = form.zip_code.data,
                favorite = form.favorite.data,
            )

            db.session.add(new_fav)
            db.session.commit()

            # get address id and add information to User_Addresses table
            new_fav = Address.query.filter(Address.address_line1==form.address_line1.data).first()

            new_ua = User_Addresses(user_id=curr_user.id, address_id=new_fav.id)
            db.session.add(new_ua)
            db.session.commit()

        except IntegrityError:
            flash('Error, try again', 'danger')
            return render_template('/favorite/add_favorite.html', form=form)
        
        flash('Successfully added new favorite', 'success')
        return redirect('/favorite/dashboard')


    return render_template('/favorite/add_favorite.html', form=form)


@app.route('/favorite/dashboard')
def show_favorites_dashboard():
    curr_user = User.query.get(session[CURR_USER_KEY])
    session_user = find_user()

    if (session_user is None):
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")

    favorites = [address for address in curr_user.addresses]

    favorites_for_api = [address.state_name for address in curr_user.addresses]
    favorites_state_data = get_multi_state_data(favorites_for_api)


    return render_template('/favorite/dashboard.html', user=curr_user, favorites=favorites, favorites_state_data=favorites_state_data)





# ******************************************************************** Testing Flask Mail

@app.route("/email")
def send_email():

    msg = Message("Hello",
                  sender="becky.schmitthenner@gmail.com",
                  recipients=["becky.schmitthenner@gmail.com"])

    msg.body = "testing"
    msg.html = "<b>testing</b>"

    mail.send(msg)

    return "<h1>MESSAGE SENT!!!</h1>"





@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
