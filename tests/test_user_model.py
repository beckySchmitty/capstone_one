"""User Model tests."""

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


class UserModelTestCase(TestCase):
    """Test user Model"""

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

        self.testuser = User.signUp(
                username="testuser",
                password="password",
                email="test@test.com",
                address_line1="123 Line One",
                address_line2="456 Line Two",
                state_name="oh",
                zip_code="43212"
        )
        self.testuser_id = 111
        self.testuser.id = self.testuser_id
        db.session.commit()


        self.client = app.test_client()


    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
# ******
# Basic Tests
# ******
    def test_user_model_basic(self):
        """Does basic model work?"""

        u = User(username="basic_user", email="test@test.com", password="password", homestate="ny")


        db.session.add(u)
        db.session.commit()

        # User should have no addresses
        self.assertEqual(len(u.addresses), 0)
        self.assertEqual(u.username, "basic_user")
        # will only be abbrv state
        self.assertNotEqual(u.homestate, "New York")

# ******
# Sign Up Tests
# ******

    def test_user_signUp(self):

        testuser = User.signUp(
                username="testuserTWO",
                password="password",
                email="test@test.com",
                address_line1="First Line",
                address_line2="Second Line",
                state_name="ny",
                zip_code="43212"
        )
        testuser_id = 000
        testuser.id = testuser_id
        db.session.commit()

        # check user is set up correctly
        u_test = User.query.get(testuser_id)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testuserTWO")
        self.assertEqual(u_test.email, "test@test.com")
        self.assertEqual(u_test.homestate, "ny")
        self.assertEqual(len(u.addresses), 1)

        # Bcrypt strings start with $2b$
        self.assertNotEqual(u_test.password, "password")
        self.assertTrue(u_test.password.startswith("$2b$"))

        # check Address also added correclty as part of signUp classmethod
        address = Address.query.filter(Address.user_id == testuser_id, Address.nickname == "homestate").one_or_none()
        self.assertIsNotNone(address)
        self.assertEqual(address.address_line1, "First Line")
        self.assertEqual(address.state_name, "ny")

    def test_invalid_username_signup(self):
        invalid_u = User.signUp(None,"password", "email@gmail.com", "street name", "apartment", "oh", "43212")
        uid = 123456789
        invalid_u.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid_u = User.signUp("usernaame","password", None, "street name", "apartment", "oh", "43212")
        uid = 123789
        invalid_u.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signUp("usernaame", None, "email@email.com", "street name", "apartment", "oh", "43212")


# ******
# Authentication Tests
# ******
    def test_valid_authentication(self):
        u = User.authenticate(self.testuser.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.testuser_id)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("falseusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.testuser.username, "falsepassword"))