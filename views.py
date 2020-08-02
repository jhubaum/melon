from flask import redirect, url_for, render_template
from . import app
from .directory import Directory

dir = Directory('/home/johannes/files/media/music')


@app.route('/')
def index():
    return redirect(url_for('show', path=""))


@app.route('/show/')
@app.route('/show/<path>')
def show(path="base"):
    if not dir.contains(path):
        return "not found", 404

    return render_template('list.html', folder=dir.get_folder(path))


@app.route('/play/<fid>')
def play(fid):
    files = dir.get_folder(fid).playlist()
    files = "".join(map(lambda x: f'<li>{x}</li>', files))
    return f'<ul>{files}</ul>'
