from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

bcrypt = Bcrypt()



class State(db.Model):
    """State"""

    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    def __repr__(self):
        return f"<User {self.username} {self.email} >"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    homestate = db.Column(db.Text, db.ForeignKey('states.name', ondelete='cascade'))

    addresses = db.relationship('Address',
                                secondary='user_addresses',
                                backref='users')

    @classmethod
    def signUp(cls, username, email, password, homestate):
        """Signs up user by hashing password & adding to database"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        new_user = User(username=username, email=email, password=hashed_pwd, homestate=homestate)
        db.session.add(new_user)
        return new_user


    @classmethod
    def authenticate(cls, username, password):
        """Find 'user' and return if password is valid"""

        user = cls.query.filter_by(username=username).first()

        if user:
            user_auth = bcrypt.check_password_hash(user.password, password)
            if user_auth:
                return user
        
        return False

    @classmethod
    def get_favs(cls, user):
        """Return user favorites or None"""
        favorites = [address for address in user.addresses if address.favorite is True]
        return favorites


class Address(db.Model):
    """Address model"""

    __tablename__ = "addresses"

    def __repr__(self):
        return f"<Address {self.user_id} {self.state_name} {self.favorite}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    address_line1 = db.Column(db.Text, nullable=False)
    address_line2 = db.Column(db.Text)
    state_name = db.Column(db.Text, db.ForeignKey('states.name', ondelete='cascade'))
    zip_code = db.Column(db.Integer, nullable=False)
    favorite = db.Column(db.Boolean, nullable=False, default=False)
    nickname = db.Column(db.Text, nullable=False,)



class User_Addresses(db.Model):
    """link user and their  addresses"""
    __tablename__ = "user_addresses"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id', ondelete='cascade'), primary_key=True)

