#!/usr/bin/python3
"""
Start a simple Flask web application.
"""

from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """
    Display "Hello HBNB!" when the root URL is accessed.
    """
    return "HELLO HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
