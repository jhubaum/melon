import os
import re

from flask import render_template, send_from_directory

FILE_TYPES = ['mp3', 'm4a', 'wma']


def _pathify(string):
    return re.sub(r'\W+', '', string.lower().replace(' ', '_'))


"""
Things I need to have
Name for the folder
Path on disk
URL
"""

class File:
    @staticmethod
    def modify_name(name):
        return re.sub(r'^[\d\s-]*', '', '.'.join(name.split('.')[:-1]))

    def __init__(self, path, name, url):
        self.name = name
        self.url = url
        self.path = path

    def render(self):
        print(self.path)
        return send_from_directory('static/music', filename=self.path)


class Folder:
    def __init__(self, path, name=None, url='', base_path=None):
        if name is None:
            self.path = os.path.join(*path)
            name = path[-1]
        else:
            self.path = path
            self.name = name
        self.url = url

        if base_path is None:
            base_path = self.path

        self.populate(base_path)

    def populate(self, base_path):
        self.folders = dict()
        self.files = dict()

        def url(fid):
            return '/'.join([self.url, fid])

        for f in sorted(os.listdir(self.path)):
            path = os.path.join(self.path, f)
            if os.path.isdir(path):
                fid = _pathify(f)
                self.folders[fid] = Folder(path, f, url(fid), base_path)
            elif f.split('.')[-1] in FILE_TYPES:
                name = File.modify_name(f)
                fid = _pathify(name)
                self.files[fid] = File(os.path.relpath(path, base_path), name,
                                       url(fid))

    def resolve(self, path):
        if path == '':
            return self

        path = path.split('/')

        it = self
        i = 0
        for i, url in enumerate(path):
            if url not in it.folders:
                break
            it = it.folders[url]
        else:
            return it

        if len(path) - i == 1:
            if len(path[i]) == 0:
                return it
            if path[i] in it.files:
                return it.files[url]

    def render(self):
        return render_template('list.html', folder=self)
