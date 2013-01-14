import os
from app import app
from app import database
from app import forms
import unittest
import tempfile

class ComptrollerTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        database.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_empty_db(self):
	rv = self.app.get('/')
	assert 'caurs!!' in rv.data

	 
    def register(self, uname, _email, inst, mjr, yr, abs_title, disc, abst): 
	rv = self.app.post('/register', data=dict(
		name=uname,
		email=_email,
		confirm_email=_email,
		institution=inst,
		major=mjr,
		year=yr,
		abstract_title=abs_title,
		discipline=disc,
		abstract=abst,), follow_redirects=True)
	return rv

    def test_register(self):
	rv = self.register("test user", "testUserEmail@mailinator.com", "depaul", "test major", 5, "test abstract title", "test academic discipline", "test abstract")
	assert 'caurs!!' in rv.data

    def test_create_Duplicate_presenter(self):
	self.register("test user", "testUserEmail@mailinator.com", "depaul",
		"test major", 4, "test abstract title", "test academic discipline", "test abstract")
	rv = self.register("test user", "testUserEmail@mailinator.com", "depaul",
		"test major", 4, "test abstract title", "test academic discipline", "test abstract")
	assert 'this shit be failing' in rv.data


if __name__ == '__main__':
    unittest.main()
