"""Seed file to make sample data for db."""

from models import User, Address, State, User_Addresses, db
from forms import states
from app import app


# Create all tables
db.drop_all()
db.create_all()

# add states
for state in states:
    state = State(name=f"{state}")
    db.session.add(state)
db.session.commit()

# Add Users
u1 = User.signUp(username="BoJack_Horseman", password="password", email="fakeemail@gmail.com", 
address_line1="123 Sunset Ave", address_line2="Apt B", state_name="ca", zip_code="99999")
u2 = User.signUp(username="BrutusTheBuckeye", password="password", email="fake2email@gmail.com", 
address_line1="321 Sunrise Ave", address_line2="Apt B", state_name="oh", zip_code="00000")
u3 = User.signUp(username="GusTheCat", password="password", email="fake3email@gmail.com", 
address_line1="888 FeedMe Ave", address_line2="Apt B", state_name="tx", zip_code="77777")

db.session.commit()


# add Addresses
a1 = Address(user_id = 1, address_line1="123 Street", state_name="ri", zip_code="43015", favorite=True, nickname="Brutus's House")
a3 = Address(user_id = 1, address_line1="789 Street", state_name="ny", zip_code="88888", favorite=True, nickname="Sister's House")
a4 = Address(user_id = 1, address_line1="112 Street", state_name="nc", zip_code="88888", favorite=False, nickname="Vacation Home")
db.session.add_all([a1, a3, a4])
db.session.commit()

#add user_addresses
ua1 = User_Addresses(user_id = 1, address_id = 4)
ua2 = User_Addresses(user_id = 1, address_id = 5)
ua3 = User_Addresses(user_id = 1, address_id = 6)

db.session.add_all([ua1, ua2, ua3])
db.session.commit()



