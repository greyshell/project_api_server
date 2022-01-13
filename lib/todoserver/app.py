import json

from flask import (
    Flask,
    make_response,
    request,
)

from .store import TaskStore, BadSummaryError


class TodoserverApp(Flask):
    store = None

    def init_db(self, engine_spec):
        self.store = TaskStore(engine_spec)

    def erase_all_test_data(self):
        assert self.testing  # if app.testing is True then execute the  next line
        self.store.delete_all_tasks()  # internal only


app = TodoserverApp(__name__)  # __name__ is used by convention, any string can be used


@app.route("/tasks/", methods=["GET"])  # a method that returns a decorator
def get_all_tasks():
    tasks = app.store.get_all_tasks()
    return make_response(json.dumps(tasks), 200)  # returns a user defined status code


@app.route("/tasks/", methods=["POST"])  # a method that returns a decorator
def create_task():
    payload = request.get_json(force=True)  # request.data.decode("utf-8")
    try:
        task_id = app.store.create_tasks(
            summary=payload["summary"],
            description=payload["description"]
        )
    except BadSummaryError:
        result = {
            "error": "Summary must be under 120 chars, without newlines"
        }
        return make_response(result, 400)

    task_info = {"id": task_id}
    return make_response(json.dumps(task_info), 201)


@app.route("/tasks/<int:task_id>/", methods=["GET"])  # a method that returns a decorator
def task_details(task_id):
    task_info = app.store.task_details(task_id)
    if task_info is None:
        return make_response("", 404)
    return make_response(json.dumps(task_info), 200)  # returns a user defined status code


@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    deleted = app.store.delete_task(task_id)
    if deleted:
        return make_response("", 200)
    return make_response("", 404)


@app.route("/tasks/<int:task_id>/", methods=["PUT"])
def modify_task(task_id):
    payload = request.get_json(force=True)
    try:
        modified = app.store.modify_task(
            task_id=task_id,
            summary=payload["summary"],
            description=payload["description"])
    except BadSummaryError:
        result = {
            "error": "Summary must be under 120 chars, without newlines"
        }
        return make_response(result, 400)
    if modified:
        return ""
    return make_response("", 404)
