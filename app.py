from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_mail import Mail, Message
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

from flask_debugtoolbar import DebugToolbarExtension 
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, State, User, Address, User_Addresses
from forms import userLoginForm, userSignUpForm, FavoriteForm, editUserForm, editHomeStateForm

from route_helpers import get_state_data, get_multi_state_data, get_formatted_date
from extra import my_password, MY_SECRET_KEY


app = Flask(__name__)


app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'beckySchmittyDev@gmail.com',
    MAIL_PASSWORD = my_password
))
# Flask-Mail
mail = Mail(app)
# Flask-Login
login = LoginManager(app)

# connect to specific database in postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_draft2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = MY_SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['TESTING'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# ********************************************************************** WELCOME 

@app.route('/')
def welcome():
    """shows homepage for all users"""
    return render_template('welcome.html', user=current_user)

# ******************************************************************** USER ROUTES

@app.route('/signup', methods=["GET", "POST"])
def handle_signup():
    """Creates user account, saves homestate address
    See @classmethod SignUp on user model"""

    form = userSignUpForm()

    if form.validate_on_submit():
        try:
            new_user = User.signUp(
                username = form.username.data,
                password = form.password.data,
                email = form.email.data,
                address_line1 = form.address_line1.data,
                address_line2 = form.address_line2.data,
                state_name = form.state_name,
                zip_code = form.zip_code.data
            )
            db.session.commit()

        except IntegrityError:
            flash('Please try again', 'danger')
            return render_template('/user/signup.html', form=form)

        login_user(user)

        return redirect('/dashboard')

    return render_template('/user/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def user_login_route():
    """Checks for user authentication, logs in user"""

    if current_user.is_authenticated:
        return redirect('/dashboard')

    form = userLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        login_user(user)

        flash(f"Welcome back, {username}!", "success")
        return redirect('/dashboard')
    else:
        flash("Invalid password, try again", "danger")

    return render_template('/user/login.html', form=form)

@app.route('/dashboard')
# @login_required
def show_home_dashboard():
    """shows main 'Home' page with homestate information"""
    if not current_user.is_authenticated:
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")

    data = get_state_data(current_user.homestate)

    return render_template('/user/dashboard.html', user=current_user, data=data)


@app.route('/user/edit', methods=["GET", "POST"])
def handle_edit_user():
    """Update user email and/or username"""

    if not current_user.is_authenticated:
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")

    form = editUserForm(obj=current_user)

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()

        flash('Account successfully updated', 'success')
        return redirect('/dashboard')

    return render_template('/user/edit.html', form=form, user=current_user)


@app.route('/homestate/edit', methods=["GET", "POST"])
def handle_homestate_edit():
    """Edit homestate address and update user.homestate"""
    if not current_user.is_authenticated:
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")

    address = Address.query.filter(Address.user_id == current_user.id, Address.nickname == "homestate").one_or_none()

    form = editHomeStateForm(obj=address)

    if form.validate_on_submit():
        address.address_line1 = form.address_line1.data,
        address.address_line2 = form.address_line2.data,
        address.state_name = form.state_name.data,
        address.zip_code = form.zip_code.data
        current_user.homestate = form.state_name.data
        db.session.commit()

        flash('Homestate address successfully updated', 'success')
        return redirect('/dashboard')

    return render_template('/user/edit_homestate.html', form=form, user=current_user)


@app.route('/logout')
def handle_user_logout():
    logout_user()
    flash("You've logged out", "success")
    return redirect('/')
  

# ******************************************************************** FAVORITE ROUTES

@app.route('/favorite/dashboard')
def show_favorites_dashboard():
    """Render 'Favorites' aka dashboard showing user favorites
    Shows Add Favorite form if none added to account"""
    if not current_user.is_authenticated:
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")

    favorites = User.get_favs(current_user)
    favorites_for_api = [address for address in favorites if address.state_name != current_user.homestate]
    # see route_helpers.py
    favorites_state_data = get_multi_state_data(favorites_for_api)

    return render_template('/favorite/dashboard.html', user=current_user, favorites_state_data=favorites_state_data)


@app.route('/favorite/add', methods=["GET", "POST"])
def handle_add_favorite_form():
    """Show add favorite form, handle form, return to dashboard"""

    if not current_user.is_authenticated:
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")

    form = FavoriteForm()

    if form.validate_on_submit():

        try: 
            new_fav = Address(
                user_id = current_user.id,
                address_line1 = form.address_line1.data,
                address_line2 = form.address_line2.data or None,
                state_name = form.state_name.data,
                zip_code = form.zip_code.data,
                favorite = True,
                nickname=form.nickname.data
            )
            db.session.add(new_fav)
            db.session.commit()

            # get address id and add information to User_Addresses table
            new_fav = Address.query.filter(Address.address_line1==form.address_line1.data).first()

            new_ua = User_Addresses(user_id=current_user.id, address_id=new_fav.id)
            db.session.add(new_ua)
            db.session.commit()

        except IntegrityError:
            flash('Error, try again', 'danger')
            return render_template('/favorite/add_favorite.html', form=form)
        
        flash('Successfully added new favorite', 'success')
        return redirect('/favorite/dashboard')


    return render_template('/favorite/add_favorite.html', form=form)


@app.route('/favorite/edit/<nickname>', methods=["GET", "POST"])
def handle_edit_favorite_form(nickname):
    """Show edit favorite form, handle form, return to dashboard"""

    if not current_user.is_authenticated:
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")

    address = Address.query.filter_by(nickname=f"{nickname}").one()
    form = FavoriteForm(obj=address)

    if form.validate_on_submit():

        try: 
            address.user_id = current_user.id
            address.address_line1 = form.address_line1.data
            address.address_line2 = form.address_line2.data or None
            address.state_name = form.state_name.data
            address.zip_code = form.zip_code.data
            address.favorite = True
            address.nickname=form.nickname.data

            db.session.commit()

        except IntegrityError:
            flash('Error, try again', 'danger')
            return render_template('/favorite/edit.html', form=form)
        
        flash(f"Successfully updated {address.nickname}", "success")
        return redirect('/favorite/dashboard')

    return render_template('/favorite/edit.html', form=form, nickname=nickname)

@app.route('/favorite/delete/<nickname>')
def delete_favorite(nickname):
    """Delete fav & redirect to favorites"""
    if not current_user.is_authenticated:
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")

    address = Address.query.filter_by(nickname=f"{nickname}").one()
    db.session.delete(address)
    db.session.commit()        

    flash(f'{address.nickname} deleted', 'success')
    return redirect('/favorite/dashboard')

# ************************************************************************* Resources

@app.route('/resources')
def show_resources():
    """shows resource page with email ability"""
    if not current_user.is_authenticated:
        flash("Unauthorized access. Please sign up or login", "danger")
        return redirect("/")

    return render_template('resources.html', user=current_user)

@app.route("/email/<user_email>")
def send_email(user_email):

    msg = Message("COVID-19 Resources (myCOVIDNumber)",
                  sender="beckySchmittyDev@gmail.com",
                  recipients=[user_email])

    msg.body = "CDC Home: https://www.cdc.gov/coronavirus/2019-ncov/index.html"
    msg.html = "<p><a href='https://www.cdc.gov/coronavirus/2019-ncov/index.html'>CDC Home</a></p><p><a href='https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/testing.html'>Learn More About Testing</a></p><p><a href='https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html'>Check Your Symptoms</a></p><p><a href='https://www.cdc.gov/coronavirus/2019-ncov/vaccines/index.html'>Learn About Vaccines</a></p><p><a href='https://www.cdc.gov/coronavirus/2019-ncov/if-you-are-sick/steps-when-sick.html'>What To Do If You're Sick</a></p><hr><p class='text-muted'>Data Source <a href='https://covidtracking.com/'>The COVID Tracking Project</a> | <a href='https://github.com/beckySchmitty'>beckySchmitty Github</a></p>"
    
    mail.send(msg)
    flash(f"Check your inbox, {user_email}", 'success')
    return redirect('/dashboard')


# ******************************************************************** Email Func

def send_myself_err_email(error):
    """Email myself errors. Created in anticipation of API changes or other edge cases"""

    msg = Message("ERROR: Capstone Project",
                  sender="beckySchmittyDev@gmail.com",
                  recipients=["becky.schmitthenner@gmail.com"])

    msg.body = f"{error}"
    msg.html = f"{error}"

    mail.send(msg)

# ******************************************************************** After

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
