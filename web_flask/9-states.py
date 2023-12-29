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


@app.route("/states")
@app.route("/states/<id>")
def list_states(id=None):
    """List all states or the cities in a particular state"""
    states_dict = storage.all(State)
    states = None
    state_obj = None
    if not id:
        states = list(storage.all(State).values())
    else:
        state_obj = states_dict.get(f"State.{id}", None)

    return render_template("9-states.html", state=state_obj, states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
