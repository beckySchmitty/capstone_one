from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

bcrypt = Bcrypt()



class State(db.Model):
    """State
    
    name is abbreviation since API only takes state abbrv"""

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
    def signUp(cls, username, password, email, address_line1, address_line2, state_name, zip_code):
        """Signs up user by hashing password & adding to database"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        new_user = User(username=username, email=email, password=hashed_pwd, homestate=state_name)
        db.session.add(new_user)
        db.session.commit()

        # grab user id after saved to database and use when saving Address
        user = cls.query.filter_by(username=username).first()
        new_address = Address(user_id=user.id, address_line1=address_line1, address_line2=address_line2, state_name=state_name, zip_code=zip_code, favorite=False, nickname="homestate")
        db.session.add(new_address)
        db.session.commit()

        # grab address id and save to User_Addresses
        address = Address.query.filter_by(nickname="homestate").first()
        ua = User_Addresses(user_id=user.id, address_id=address.id)
        db.session.add(ua)
        db.session.commit()

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
    nickname = db.Column(db.Text, nullable=False)


class User_Addresses(db.Model):
    """link user and their  addresses"""
    __tablename__ = "user_addresses"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id', ondelete='cascade'), primary_key=True)

