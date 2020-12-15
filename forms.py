from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired, Optional, Email

states = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj', 'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy', 'as', 'fm', 'mh', 'mp', 'pr', 'pw', 'vi' ]

class userSignUpForm(FlaskForm):
    """Form to sign up user"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    address_line1 = StringField('Address Line 1', validators=[DataRequired()])
    address_line2 = StringField('Address Line 2', validators=[Optional()])
    state_name = SelectField('State',validators=[DataRequired()], choices=[(state, state.upper()) for state in states])
    zip_code = FloatField('Zip Code', validators=[DataRequired()])

class userLoginForm(FlaskForm):
    """Form to login"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class editUserForm(FlaskForm):
    """form to edit user"""

    email = StringField('E-mail', validators=[Optional(), Email()])
    username = StringField('Username', validators=[Optional()])


class FavoriteForm(FlaskForm):
    """form for users to add favorites"""

    address_line1 = StringField('Address Line 1', validators=[DataRequired()])
    address_line2 = StringField('Address Line 2', validators=[Optional()])
    state_name = SelectField('Home State',validators=[DataRequired()], choices=[(state, state.upper()) for state in states])
    zip_code = FloatField('Zip Code', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])

class editHomeStateForm(FlaskForm):
    """Edit Homestate"""
    address_line1 = StringField('Address Line 1', validators=[DataRequired()])
    address_line2 = StringField('Address Line 2', validators=[Optional()])
    state_name = SelectField('State',validators=[DataRequired()], choices=[(state, state.upper()) for state in states])
    zip_code = FloatField('Zip Code', validators=[DataRequired()])