from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension 
from models_two import db, connect_db, User, Address, State, get_favs

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
def home():
    """shows homepage"""
    return render_template('home.html')

@app.route('/dashboard')
def home():
    """shows homepage"""


    return render_template('')


