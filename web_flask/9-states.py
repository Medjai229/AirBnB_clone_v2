#!/usr/bin/python3
"""This script starts a Flask web application"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states(id=None):
    """renders an html page with listed states"""
    states = storage.all("State")
    if id is None:
        return render_template("9-states.html", state=states)
    else:
        for state in states.values():
            if state.id == id:
                return render_template("9-states.html", state=state)
        return render_template("9-states.html")


@app.teardown_appcontext
def teardown_db(execute):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
