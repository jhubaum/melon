from flask import url_for, render_template, send_from_directory
from . import app
from .directory import Folder


dir = Folder([app.static_folder, 'music'])


@app.route('/')
@app.route('/<path:path>')
def show(path=''):
    r = dir.resolve(path)

    if r is None:
        return "not found", 404

    return r.render()


@app.route('/play/<fid>')
def play(fid):
    if not dir.contains(fid):
        return "not found", 404

    return render_template('play.html', folder=dir.get_folder(fid))

@app.route('/tracks/<path:path>')
def get_track(path):
    print(app.static_folder, path.split('/'))
    return send_from_directory('static/music',
                               filename="alpha_waves.mp3",
                               as_attachment=True)
