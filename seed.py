"""Seed file to make sample data for db."""

from models import User, Address, State, User_Addresses, db
from app import app

# Create all tables
db.drop_all()
db.create_all()


# add states
s1 = State(name="oh")
s2 = State(name="ca")
s3 = State(name="ny")
s4 = State(name="nc")
db.session.add_all([s1, s2, s3, s4])
db.session.commit()

# Add Users
u1 = User.signUp(username="BoJack Horseman", email="fakeemail@gmail.com", password="password", homestate="oh")
u2 = User.signUp(username="Julia Andrews", email="fake2@gmail.com", password="password", homestate="ny")
u3 = User.signUp(username="Brutus theBuckeye", email="fake3@gmail.com", password="password", homestate="ca")
db.session.commit()


# add Addresses
a1 = Address(user_id = 1, address_line1="fake", state_name="oh", zip_code="43015", favorite=False)
a2 = Address(user_id = 1, address_line1="fake", state_name="ca", zip_code="99999", favorite=True)
a3 = Address(user_id = 1, address_line1="fake", state_name="ny", zip_code="88888", favorite=True)
db.session.add_all([a1, a2, a3])
db.session.commit()

#add user_addresses
ua1 = User_Addresses(user_id = 1, address_id = 1)
ua2 = User_Addresses(user_id = 1, address_id = 2)
ua3 = User_Addresses(user_id = 1, address_id = 3)
db.session.add_all([ua1, ua2, ua3])
db.session.commit()



