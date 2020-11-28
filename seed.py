"""Seed file to make sample data for db."""

from models_two import User, Address, State, db
from app_two import app

# Create all tables
db.drop_all()
db.create_all()


# add states
s1 = State(name="oh")
s2 = State(name="ca")
s3 = State(name="ny")
s4 = State(name="nc")
db.session.add_all([s1, s2, s3])
db.session.commit()


# Add Users
u1 = User(username="BoJack Horseman", email="fakeemail@gmail.com", password="password", homestate="oh")
u2 = User(username="Julia Andrews", email="fake2@gmail.com", password="password", homestate="ny")
u3 = User(username="Brutus theBuckeye", email="fake3@gmail.com", password="password", homestate="ca")
db.session.add_all([u1, u2, u3])
db.session.commit()


# add Addresses
a1 = Address(user_id=1, state_name="oh", favorite=True)
a2 = Address(user_id=2, state_name="ny", favorite=False)
a3 = Address(user_id=1, state_name="ny", favorite=True)
a4 = Address(user_id=3, state_name="ca", favorite=False)
a4 = Address(user_id=3, state_name="oh", favorite=False)
a5 = Address(user_id=1, state_name="ca", favorite=True)
a6 = Address(user_id=1, state_name="nc", favorite=False)
db.session.add_all([a1, a2, a3, a4, a5, a6])
db.session.commit()

