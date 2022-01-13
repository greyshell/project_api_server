import unittest
import json
from todoserver import app
# echo $PYTHONPATH = /Users/abhijitsinha/Documents/project_api_server/lib

# enable more debugging info
app.testing = True  # disable in production
app.init_db("sqlite:///:memory:")


def json_body(resp):
    return json.loads(resp.data.decode("utf-8"))


class TestTodoserver(unittest.TestCase):

    # helper method
    def create_test_task(self, summary="Get milk", description="One gallon organic whole milk"):
        # create a new task to modify
        new_task_data = {
            "summary": summary,
            "description": description
        }
        resp = self.client.post("/tasks/",
                                data=json.dumps(new_task_data))
        self.assertEqual(201, resp.status_code)

        # get the task details
        return json_body(resp)

    def setUp(self):
        app.erase_all_test_data()
        self.client = app.test_client()
        # verify the test pre-condition
        resp = self.client.get("/tasks/")  # mapped -> @app.route("/tasks/")
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], json_body(resp))

    def test_create_a_task_and_get_its_details(self):
        # create a task
        data = self.create_test_task()
        self.assertIn("id", data)

        # get the task details
        task_id = data["id"]
        resp = self.client.get("/tasks/{:d}/".format(task_id))  # :d -> type assertion
        self.assertEqual(200, resp.status_code)

        task = json_body(resp)
        self.assertEqual(task_id, task["id"])
        self.assertEqual("Get milk", task["summary"])
        self.assertEqual("One gallon organic whole milk", task["description"])

    def test_create_multiple_tasks_and_fetch_list(self):
        tasks = [
            (201, {"summary": "Get milk", "description": "Half gallon of almond milk"}),
            (201, {"summary": "Go to gym", "description": "Leg day. Blast those quads!"}),
            (201, {"summary": "Wash car", "description": "Be sure to get wax coat"}),
        ]

        for expected, kwargs in tasks:
            with self.subTest(**kwargs):
                resp = self.client.post("/tasks/",
                                        data=json.dumps(kwargs))
                self.assertEqual(expected, resp.status_code)

        # # get list of tasks
        resp = self.client.get("/tasks/")
        self.assertEqual(200, resp.status_code)
        checked_tasks = json_body(resp)
        self.assertEqual(3, len(checked_tasks))

    def test_delete_task(self):
        # create a task and get the task details
        task_id = self.create_test_task()["id"]
        # delete the task
        resp = self.client.delete("/tasks/{:d}/".format(task_id))  # :d -> type assertion
        self.assertEqual(200, resp.status_code)

        # verify the task is really gone
        resp = self.client.get("/tasks/{:d}/".format(task_id))
        self.assertEqual(404, resp.status_code)

    def test_modify_existing_task(self):
        # create a new task to modify
        task_id = self.create_test_task()["id"]

        # update it
        updated_task_data = {
            "summary": "Get almond milk",
            "description": "Half gallon, vanilla flavored",
        }
        resp = self.client.put(
            "/tasks/{:d}/".format(task_id),
            data=json.dumps(updated_task_data))
        self.assertEqual(200, resp.status_code)
        # verify change
        resp = self.client.get("/tasks/{:d}/".format(task_id))
        check_task = json_body(resp)
        self.assertEqual(
            updated_task_data["summary"],
            check_task["summary"])
        self.assertEqual(
            updated_task_data["description"],
            check_task["description"])

    def test_error_when_getting_nonexisting_task(self):
        resp = self.client.get("/tasks/42/")
        self.assertEqual(404, resp.status_code)

    def test_error_when_deleting_nonexisting_task(self):
        resp = self.client.delete("/tasks/42/")
        self.assertEqual(404, resp.status_code)

    def test_error_when_updating_nonexisting_task(self):
        data = {
            "summary": "",
            "description": "",
        }
        resp = self.client.put("/tasks/42/",
                               data=json.dumps(data))
        self.assertEqual(404, resp.status_code)

    def test_error_when_creating_task_with_bad_summary(self):
        bad_summaries = [
            "x" * 120,
            "foo\nbar"
        ]
        for bad_summary in bad_summaries:
            with self.subTest(bad_summary=bad_summary):

                task_info = {
                    "summary": bad_summary,
                    "description": "",
                }
                resp = self.client.post("/tasks/",
                                        data=json.dumps(task_info))
                self.assertEqual(400, resp.status_code)
                result = json_body(resp)
                self.assertIn("error", result)
                self.assertEqual(
                    "Summary must be under 120 chars, without newlines",
                    result["error"])
