"""User Model tests."""

# run these tests like:
#    FLASK_ENV=production python -m unittest test_user_model.py

import os
from unittest import TestCase

from models import db, connect_db, User, Address, User_Addresses
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

        self.testuser = User.signUp(username="testuser",
                                    email="test@test.com",
                                    password="password",
                                    homestate="oh")
        self.testuser_id = 111
        self.testuser.id = self.testuser_id

        self.testuser_two = User.signUp(username="testuser_two",
                                    email="test@test.com",
                                    password="password",
                                    homestate="ny")
        self.testuser_two_id = 222
        self.testuser_two.id = self.testuser_two_id

        db.session.commit()

        testuser = User.query.get(testuser_id)
        testuser_two = User.query.get(testuser_two_id)

        self.testuser = testuser
        self.testuser_id = testuser_id

        self.testuser_two = testuser_two
        self.testuser_two_id = testuser_two_id

        self.client = app.test_client()


    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

            """Does basic model work?"""

    def test_user_model_basic(self):
           u = User(username="basic_user", email="test@test.com", password="password", homestate="ny")

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)