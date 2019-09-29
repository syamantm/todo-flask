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
        self.client = app.test_client()
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
        return self.client.post(
            '/tasks',
            data=json.dumps(dict(title=title, description=description)),
            content_type='application/json'
        )

    def get_task(self, task_id):
        return self.client.get(
            f'/tasks/{task_id}'
        )

    def get_all_tasks(self):
        return self.client.get(
            f'/tasks'
        )

    def update_task(self, task_id, payload):
        return self.client.put(
            f'/tasks/{task_id}',
            data=json.dumps(payload),
            content_type='application/json'
        )

    def delete_task(self, task_id):
        return self.client.delete(
            f'/tasks/{task_id}'
        )

    ###############
    #### tests ####
    ###############

    def test_add_task_is_successful(self):
        response = self.add_task(title="test task", description="test task")
        self.assertEqual(response.status_code, 201)

    def test_add_task_rejects_non_json_payload(self):
        response = self.client.post(
            '/tasks',
            data="a non json payload"
        )
        self.assertEqual(response.status_code, 400)

    def test_get_task_is_successful(self):
        response = self.add_task(title="test task", description="test task")
        self.assertEqual(response.status_code, 201)
        task_id = json.loads(response.data)["id"]
        task_response = self.get_task(task_id)
        self.assertEqual(task_response.status_code, 200)

    def test_get_task_handles_unknown_task_id(self):
        get_response = self.get_task(342342342)
        self.assertEqual(get_response.status_code, 404)

    def test_get_all_tasks_is_successful(self):
        r1 = self.add_task(title="test task 1", description="test task")
        r2 = self.add_task(title="test task 2", description="test task")
        all_tasks = self.get_all_tasks()
        self.assertEqual(all_tasks.status_code, 200)
        self.assertEqual(len(json.loads(all_tasks.data)["tasks"]), 2)

    def test_update_task_updates_title(self):
        response = self.add_task(title="test task", description="test task")
        self.assertEqual(response.status_code, 201)
        task_id = json.loads(response.data)["id"]
        update_response = self.update_task(task_id, {"title": "updated title"})
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(json.loads(update_response.data)["title"], "updated title")

    def test_update_task_updates_description(self):
        response = self.add_task(title="test task", description="test task")
        self.assertEqual(response.status_code, 201)
        task_id = json.loads(response.data)["id"]
        update_response = self.update_task(task_id, {"description": "updated description"})
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(json.loads(update_response.data)["description"], "updated description")

    def test_update_task_updates_done(self):
        response = self.add_task(title="test task", description="test task")
        self.assertEqual(response.status_code, 201)
        task_id = json.loads(response.data)["id"]
        update_response = self.update_task(task_id, {"done": True})
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(json.loads(update_response.data)["done"], True)

    def test_update_task_handles_unknown_task_id(self):
        update_response = self.update_task(342342342, {"done": True})
        self.assertEqual(update_response.status_code, 404)

    def test_update_task_handles_non_json_payload(self):
        response = self.add_task(title="test task", description="test task")
        self.assertEqual(response.status_code, 201)
        task_id = json.loads(response.data)["id"]
        update_response = self.client.put(
            f'/tasks/{task_id}',
            data="a non json payload"
        )
        self.assertEqual(update_response.status_code, 400)

    def test_update_task_rejects_done_with_non_boolean_value(self):
        response = self.add_task(title="test task", description="test task")
        self.assertEqual(response.status_code, 201)
        task_id = json.loads(response.data)["id"]
        update_response = self.update_task(task_id, {"done": "true"})
        self.assertEqual(update_response.status_code, 400)

    def test_delete_task_is_successful(self):
        response = self.add_task(title="test task", description="test task")
        self.assertEqual(response.status_code, 201)
        task_id = json.loads(response.data)["id"]
        delete_response = self.delete_task(task_id)
        self.assertEqual(delete_response.status_code, 200)

    def test_delete_task_handles_unknown_task_id(self):
        delete_response = self.delete_task(342342342)
        self.assertEqual(delete_response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
