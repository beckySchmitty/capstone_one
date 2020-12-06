"""User Model tests."""

# run these tests like:
#    FLASK_ENV=production python -m unittest test_user_model.py

import os
from unittest import TestCase

from models import db, connect_db, User, Address, User_Addresses, State
from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = "postgresql:///capstone-draft-tests"

from app import app, CURR_USER_KEY

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

        self.testuser = User.signUp(username="testuser",
                                    email="test@test.com",
                                    password="password",
                                    homestate="oh")
        self.testuser_id = 111
        self.testuser.id = self.testuser_id

        self.testuser_two = User.signUp(username="testuser_two",
                                    email="test2@test.com",
                                    password="password",
                                    homestate="ny")
        self.testuser_two_id = 222
        self.testuser_two.id = self.testuser_two_id

        db.session.commit()

        testuser = User.query.get(self.testuser_id)
        testuser_two = User.query.get(self.testuser_two_id)

        self.testuser = testuser
        self.testuser_id = self.testuser_id

        self.testuser_two = testuser_two
        self.testuser_two_id = self.testuser_two_id

        self.client = app.test_client()


    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_user_model_basic(self):
        """Does basic model work?"""

        u = User(username="basic_user", email="test@test.com", password="password", homestate="ny")

        db.session.add(u)
        db.session.commit()

        # User should have no addresses
        self.assertEqual(len(u.addresses), 0)
        self.assertEqual(u.username, "basic_user")