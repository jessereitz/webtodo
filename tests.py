#!flask/bin/python

import os
import unittest

from config import Test_Config
from app import app, db
from app.models import User

class UserTest(unittest.TestCase):
    def setUp(self):
        app.config.from_object(Test_Config)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testCreateUser(self):
        user1 = User(username="user1", password="password")
        user2 = User(username="user2", password="password")

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        assert user1.id != None
        assert user2.id != None

        users = User.query.all()
        assert len(users) == 2


if __name__ == '__main__':
    unittest.main()
