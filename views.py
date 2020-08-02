from flask import redirect, url_for
from . import app

@app.route('/')
def index():
    return redirect(url_for('show', path=""))

@app.route('/show/')
@app.route('/show/<path>')
def show(path=""):
    return "Setup successful"
