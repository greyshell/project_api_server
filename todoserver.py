from flask import Flask, make_response

app = Flask(__name__)  # __name__ is used by convention, any string can be used


@app.route("/tasks/")  # a method that returns a decorator
def get_all_tasks():
    # return json response
    return make_response("[]", 200)  # returns a user defined status code


if __name__ == "__main__":
    app.run()
