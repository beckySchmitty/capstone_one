from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension 
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Address, State, get_favs
from forms import userLoginForm, userSignUpForm



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
        
        session['CURRENT_USER'] = new_user.username

        return redirect('/home')

    return render_template('/user/signup.html', form=form)


@app.route('/home')
def show_home_dashboard():
    """shows dashboard with homestate information"""
    username = session['CURRENT_USER']
    user = User.query.filter(User.username == username).first()


    return render_template('/user/home.html', user=user)


