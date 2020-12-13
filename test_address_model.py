"""Address Model tests."""

#    FLASK_ENV=production python -m unittest test_address_model.py

import os
from unittest import TestCase
from sqlalchemy import exc


from models import db, connect_db, State, User, Address, User_Addresses
from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = "postgresql:///capstone-draft-tests"

from app import app, CURR_USER_KEY
db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test
# UPDATE_LATER - figure out how to test CSRF when I have more time
app.config['WTF_CSRF_ENABLED'] = False


class AddressModelTestCase(TestCase):
    """Test Address Model"""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        # add states
        s1 = State(name="oh")
        s2 = State(name="ca")
        s3 = State(name="ny")
        s4 = State(name="nc")
        db.session.add_all([s1, s2, s3, s4])
        db.session.commit()

        user = User.signUp(
                username="testuser",
                password="password",
                email="test@test.com",
                address_line1="123 Line One",
                address_line2="456 Line Two",
                state_name="oh",
                zip_code="43212"
        )
        db.session.add(user)
        db.session.commit()

        self.user = User.query.filter_by(username="testuser").one()
        user.id = 111
        self.user_id = user.id

        self.testaddress = Address(
                user_id=user_id
                address_line1="First Street",
                address_line2="Apt A",
                state_name="ny",
                zip_code="99999",
                favorite=True,
                nickname="Sister's House"
        )
        self.testaddress_id = 999
        self.testaddress.id = self.testaddress_id
        db.session.commit()


        self.client = app.test_client()


    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
# ******
# Basic Tests
# ******
    def test_basic_Address_model(self):
        """Does basic model work?"""

        a = Address(
                user_id=self.user_id
                address_line1="Rocket Drive",
                address_line2="Apt R",
                state_name="ca",
                zip_code="88888",
                favorite=True,
                nickname="Fred's House"
        )

        db.session.add(a)
        db.session.commit()

        self.assertIsNotNone(a)
        self.assertEqual(a.favorite, True)
        self.assertNotEqual(a.address_line1, "Rocket Drive")

        self.assertIn("Rocket Drive",self.user.addresses[1].address_line1)
