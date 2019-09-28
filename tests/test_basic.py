import os
import unittest
import json
from app import app, db


TEST_DB = 'test.db'
basedir = os.path.abspath(os.path.dirname(__file__))


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ########################
    #### helper methods ####
    ########################

    def add_task(self, title, description):
        return self.app.post(
            '/tasks',
            data=json.dumps(dict(title=title, description=description)),
            content_type='application/json'
        )

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_task_is_successful(self):
        response = self.add_task(title="test task", description="test task")
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()