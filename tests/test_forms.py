import sys
import unittest

sys.path.append('../')
from flask_mysqldb import MySQL

from project import app


class FormTests(unittest.TestCase):
    # Setup and Teardown
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    # Tests
    def test_db_connection(self):
        with app.app_context():
            mysql = MySQL(app)
            cursor = mysql.connection.cursor()


if __name__ == "__main__":
    unittest.main()
