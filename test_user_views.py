"""User View tests."""

#    FLASK_ENV=production python -m unittest test_user_views.py

import os
from unittest import TestCase

from models import db, connect_db, State, User, Address, User_Addresses
from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = "postgresql:///capstone-draft-tests"

# import after envir setup
from app import app, CURR_USER_KEY

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test
# UPDATE_LATER - figure out how to test CSRF when I have more time
app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        # add states
        s1 = State(name="oh")
        s2 = State(name="ca")
        s3 = State(name="ny")
        s4 = State(name="nc")
        db.session.add_all([s1, s2, s3, s4])
        db.session.commit()

        # add test users
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

        self.testuser = User.signUp(
                username="testusertwo",
                password="password",
                email="tes2t@test.com",
                address_line1="123 Line One",
                address_line2="456 Line Two",
                state_name="ny",
                zip_code="43212"
        )
        self.testuser_two_id = 222
        self.testuser_two.id = self.testuser_two_id

        db.session.commit()

        testuser = User.query.get(self.testuser_id)
        testuser_two = User.query.get(self.testuser_two_id)

        self.testuser = testuser
        self.testuser_id = self.testuser_id

        self.testuser_two = testuser_two
        self.testuser_two_id = self.testuser_two_id

        self.u3 = User.signUp("three_user", "test3@test.com", "password", "ca")
        self.u4 = User.signUp("four_user", "test4@test.com", "password", "ca")

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def user_login(self):
        with self.client as client:
            resp = client.post('/login', data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"Welcome back, {self.username}", str(resp.data))
            self.assertNotEqual("Invalid password, try again", str(resp.data))

    def bad_login(self):
        with self.client as client:
            resp = client.post('/login', data=dict(
            username=self.username,
            password="incorrectpassword"
        ), follow_redirects=True)

            self.assertEqual(resp.status_code, 304)
            self.assertNotEqual(f"Welcome back, {self.username}", str(resp.data))
            self.assertIn("Invalid password, try again", str(resp.data))

    def show_dashboard(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = client.get('/dashboard', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual("Ohio", str(resp.data))
            self.assertEqual("Cases", str(resp.data))
            self.assertEqual("Hospitalizations", str(resp.data))
            self.assertNotEqual("Invalid", str(resp.data))

    def show_user_edit_form(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = client.get('/user/edit', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual("Update Your Account", str(resp.data))
            self.assertEqual("Email", str(resp.data))
            self.assertEqual("Username", str(resp.data))
            self.assertNotEqual(404, str(resp.data))
            self.assertNotEqual("Invalid", str(resp.data))

    def handle_user_edit(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            user = User.query,get(self.testuser_id)    

            resp = client.post('/user/edit', data=dict(
            email="newemail@gmail.com",
            username="ca"
        ), follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(user.email, "newemail@gmail.com")
            self.assertNotEqual(user.email, "firstemail@gmail.com")
            self.assertEqual("Account successfully updated", str(resp.data))
            self.assertNotEqual("Invalid", str(resp.data))





