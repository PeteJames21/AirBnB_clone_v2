#!/usr/bin/python3
"""
Hello world using Flask
"""

from flask import Flask
from markupsafe import escape

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def index():
    """The root page"""
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    """The /hbnb page"""
    return "HBNB"


@app.route("/c/<text>")
def c(text):
    """The /c page"""
    # Return "C " followed by the value of the `text` query parameter
    # Underscores are replaced with spaces
    text = escape(text.replace("_", " "))
    return f"C {text}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
