#!/usr/bin/python3
""" module doc for a  web application must 
be listening on 0.0.0.0, port 5000
and must have /states_list route to display a HTML page """

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ Returns a simple greeting message. """
    return "Hello HBNB!"



@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Returns a string 'HBNB'. """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ Returns the string 'c' followed by the modified
    `text` parameter, replacing underscores with spaces. """
    return 'c {}'.format(text.replace("_", " "))


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    """ Returns the string 'Python' followed by the
    modified `text` parameter, replacing underscores with spaces. """
    return 'Python {}'.format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ Returns a string indicating that
    the provided integer `n` is a number. """
    return '{} is a number'.format(n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """ Renders a template that displays whether
    the number `n` is odd or even. """
    if n % 2 == 0:
        p = 'even'
    else:
        p = 'odd'
    return render_template('6-number_odd_or_even.html', number=n, parity=p)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ Renders a template that lists states
    retrieved from the storage. """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def close(error):
    """ Closes the database connection at the
    end of the request or when the application shuts down. """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
