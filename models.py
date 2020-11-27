from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class State(db.Model):
    """State"""

    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    def __repr__(self):
        return f"<User {self.name} {self.email} >"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    hometown = db.Column(db.Text, db.ForeignKey('states.name'))


    # Direct relationship
    addresses = db.relationship('Address', backref='user')

    # states = db.relationship('State', backref='users')



class Address(db.Model):
    """Address model"""

    __tablename__ = "Addresses"

    def __repr__(self):
        return f"<Adress {self.user_id} {self.state_name} {self.favorite} >"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    state_name = db.Column(db.Text, db.ForeignKey('states.name'))
    favorite = db.Column(db.Boolean, nullable=False, default=False)



def get_favs(user_id):
    user = User.query.get(user_id)

    for address in user.addresses:
        if address.favorite is True:
            return [address.state_name for address in user.addresses if address.state_name != user.hometown]
        else:
            return "No Favorites"

