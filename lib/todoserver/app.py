import json

from flask import (
    Flask,
    make_response,
    request,
)

app = Flask(__name__)  # __name__ is used by convention, any string can be used

MEMORY = {}


@app.route("/tasks/", methods=["GET"])  # a method that returns a decorator
def get_all_tasks():
    # a list of dictionaries: list comprehension
    tasks = [
        {"id": task_id, "summary": task["summary"]}
        for task_id, task in MEMORY.items()
    ]
    return make_response(json.dumps(tasks), 200)  # returns a user defined status code


@app.route("/tasks/", methods=["POST"])  # a method that returns a decorator
def create_task():
    payload = request.get_json(force=True)  # request.data.decode("utf-8")

    try:
        task_id = 1 + int(max(MEMORY.keys()))
    except ValueError:  # when MEMORY.keys() is empty
        task_id = 1

    MEMORY[task_id] = {
        "summary": payload["summary"],
        "description": payload["description"]
    }
    task_info = {
        "id": task_id
    }
    return make_response(json.dumps(task_info), 201)


@app.route("/tasks/<int:task_id>/", methods=["GET"])  # a method that returns a decorator
def task_details(task_id):
    task_info = MEMORY[task_id].copy()
    task_info["id"] = task_id

    return make_response(json.dumps(task_info), 200)  # returns a user defined status code
