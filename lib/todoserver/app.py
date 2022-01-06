import json

from flask import (
    Flask,
    make_response,
    request,
)

from .store import TaskStore


class TodoserverApp(Flask):
    def __init__(self, name):
        self.store = TaskStore()
        super().__init__(name)


app = TodoserverApp(__name__)  # __name__ is used by convention, any string can be used


@app.route("/tasks/", methods=["GET"])  # a method that returns a decorator
def get_all_tasks():
    tasks = app.store.get_all_tasks()
    return make_response(json.dumps(tasks), 200)  # returns a user defined status code


@app.route("/tasks/", methods=["POST"])  # a method that returns a decorator
def create_task():
    payload = request.get_json(force=True)  # request.data.decode("utf-8")
    task_id = app.store.create_tasks(
        summary=payload["summary"],
        description=payload["description"]
    )
    task_info = {"id": task_id}
    return make_response(json.dumps(task_info), 201)


@app.route("/tasks/<int:task_id>/", methods=["GET"])  # a method that returns a decorator
def task_details(task_id):
    task_info = app.store.task_details(task_id)
    return make_response(json.dumps(task_info), 200)  # returns a user defined status code
