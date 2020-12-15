"""Favorite Views tests."""

import os
from unittest import TestCase

from models import db, connect_db, State, User, Address, User_Addresses
from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = "postgresql:///capstone-draft-tests"

# import after envir setup
from app import app
from flask_login import current_user


db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test
# UPDATE_LATER - figure out how to test CSRF when I have more time
app.config['WTF_CSRF_ENABLED'] = False


class FavoriteViewTestCase(TestCase):
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
        self.testuser = User.signUp(username="BoJack_Horseman", password="password", email="fakeemail@gmail.com", 
        address_line1="123 Sunset Ave", address_line2="Apt B", state_name="ca", zip_code="99999")
        db.session.commit()

        self.testuser = User.query.get(self.testuser.id)

        self.testuser_id = 111
        self.testuser.id = self.testuser_id
        db.session.commit()

        a1 = Address(user_id = self.testuser_id, address_line1="123 Street", state_name="ri", zip_code="43015", favorite=True, nickname="Brutus's House")
        a3 = Address(user_id = self.testuser_id, address_line1="789 Street", state_name="ny", zip_code="88888", favorite=False, nickname="Sister's House")
        a4 = Address(user_id = self.testuser_id, address_line1="112 Street", state_name="nc", zip_code="88888", favorite=True, nickname="Vacation Home")
        db.session.add_all([a1, a3, a4])
        db.session.commit()

        ua1 = User_Addresses(user_id = self.testuser_id, address_id = 4)
        ua2 = User_Addresses(user_id = self.testuser_id, address_id = 5)
        ua3 = User_Addresses(user_id = self.testuser_id, address_id = 6)

        db.session.add_all([ua1, ua2, ua3])
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def show_fav_dashboard(self):
         with self.client as client:
            resp = client.get('/favorite/dashboard', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual("Plan travel or inform loved ones", str(resp.data))
            self.assertEqual("Favorites", str(resp.data))
            self.assertNotEqual(404, str(resp.data))
            self.assertNotEqual("You haven't added any favorites yet", str(resp.data))

    def show_edit_fav(self):
        with self.client as client:
            resp = client.get("/favorite/edit/Brutus's%20House", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual("Update Vacation Home", str(resp.data))
            self.assertEqual("Save", str(resp.data))
            self.assertEqualNotEqual("Favorites", str(resp.data))
            self.assertNotEqual(404, str(resp.data))

    def handle_edit_fav(self):
        with self.client as client:
            resp = client.post("/favorite/edit/Brutus's%20House", data=dict(
            address_line1="New Stree Name", 
            state_name="tx", 
            zip_code="99999",
            nickname="Brutus's House")
        , follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual("Successfully updated favorite", str(resp.data))
            self.assertEqual("Texas", str(resp.data))
            self.assertNotEqual("Invalid", str(resp.data))

    def delete_fav(self):
        with self.client as client:

            resp = client.get("/favorite/delete/Brutus's%20House", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual("Brutus's House deleted", str(resp.data))
            self.assertNotRqual("Texas", str(resp.data))
            self.assertNotEqual("Invalid", str(resp.data))
