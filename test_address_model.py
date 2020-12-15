"""Address Model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc


from models import db, connect_db, State, User, Address, User_Addresses
from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = "postgresql:///capstone-draft-tests"

from app import app
from flask_login import current_user


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

        self.user = User.signUp(
                username="testuser",
                password="password",
                email="test@test.com",
                address_line1="123 Line One",
                address_line2="456 Line Two",
                state_name="oh",
                zip_code="43212"
        )
        db.session.add(self.user)
        db.session.commit()

        self.a1 = Address(
                user_id=self.user.id,
                address_line1="First Street",
                address_line2="Apt A",
                state_name="ny",
                zip_code="99999",
                favorite=True,
                nickname="Sister's House"
        )

        db.session.add(self.a1)
        db.session.commit()

        ua = User_Addresses(user_id=self.user.id, address_id=self.a1.id)
        db.session.add(ua)
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

        self.assertIsNotNone(self.a1)
        self.assertEqual(self.a1.favorite, True)
        self.assertEqual(self.a1.address_line1, "First Street")
        self.assertEqual(self.a1.address_line2, "Apt A")


        self.assertIn("First Street", self.user.addresses[1].address_line1)
        self.assertIn("Apt A", self.user.addresses[1].address_line2)
        self.assertIn(self.a1, self.user.addresses)

        self.assertIn("123 Line One", self.user.addresses[0].address_line1)
        self.assertEqual(False, self.user.addresses[0].favorite)