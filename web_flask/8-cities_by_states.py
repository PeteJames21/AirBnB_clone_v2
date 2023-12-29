#!/usr/bin/python3
"""
Run a Flask app that serves a list of cities in each state.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(error):
    storage.close()


@app.route("/cities_by_states")
def cities_by_states():
    """List each state and its cities"""
    states = list(storage.all(State).values())
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
