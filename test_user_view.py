"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, User, Address, User_Addresses
from bs4 import BeautifulSoup

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///capstone-draft-tests"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test
# UPDATE_LATER - figure out how to test CSRF when I have more time
app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.testuser = User.signUp(username="testuser",
                                    email="test@test.com",
                                    password="password",
                                    homestate="oh")
        self.testuser_id = 999
        self.testuser.id = self.testuser_id

        self.u1 = User.signUp("one_user", "test1@test.com", "password", "ca")
        self.u1_id = 111
        self.u1.id = self.u1_id
        self.u2 = User.signUp("two_user", "test2@test.com", "password", "ca")
        self.u2_id = 222
        self.u2.id = self.u2_id
        self.u3 = User.signUp("three_user", "test3@test.com", "password", "ca")
        self.u4 = User.signUp("four_user", "test4@test.com", "password", "ca")

        self.client = app.test_client()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def user_login(self):
        with self.client as client:
            resp = c.post('/login', data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"Welcome back, {self.username}", str(resp.data))

    def bad_login(self):
        with self.client as client:
            resp = c.post('/login', data=dict(
            username=self.username,
            password="badpassword"
        ), follow_redirects=True)

            self.assertEqual(resp.status_code, 304)
            self.assertNotEqual(f"Welcome back, {self.username}", str(resp.data))
            self.assertIn("Invalid password, try again", str(resp.data))



