import unittest
import sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app import app

class TestHello(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home_page(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '404 NOT FOUND')

    def test_unauthorized_access(self):
        rv = self.app.get('/meals/1')
        self.assertEqual(rv.status, '401 UNAUTHORIZED')

    # def test_login_endpoint(self):
    #     rv = self.app.post('/register?username=admin&password=admin123')
    #     self.assertEqual(rv.status, "200 OK")

if __name__ == '__main__':
    unittest.main()