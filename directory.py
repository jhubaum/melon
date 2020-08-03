import os
import re

FILE_TYPES = ['mp3', 'm4a', 'wma']


def _pathify(string):
    return re.sub(r'\W+', '', string.lower().replace(' ', '_'))


"""
Things I need to have
Name for the folder
Path on disk
URL
"""
class Folder:
    def __init__(self, *path_parts, url=[]):
        self.path = os.path.join(*path_parts)
        self.name = path_parts[-1]
        self.url = '/'.join(url)

        self.folders = dict()
        self.files = dict()

        for f in os.listdir(self.path):
            p = os.path.join(self.path, f)
            p_f = _pathify(f)
            if os.path.isdir(p):
                self.folders[p_f] = Folder(p,
                                           url=[self.url, p_f])

            elif f.split('.')[-1] in FILE_TYPES:
                self.files[p_f] = f

    def resolve_folder(self, url):
        if url == '':
            return self

        it = self
        for url in url.split('/'):
            if url not in it.folders:
                return None
            it = it.folders[url]
        return it


"""
class Folder:
    def __init__(self, fid, path, name):
        self.fid = fid
        self.path = path
        self.name = name

        self.dirs = []
        self.files = []

    def _parse_children(self, folders, tracks):
        for f in os.listdir(self.path):
            p = os.path.join(self.path, f)
            if os.path.isdir(p):
                new = Folder(len(folders), p, f)
                folders[str(new.fid)] = new
                self.dirs.append(new)
                yield new
            elif f.split('.')[-1] in FILE_TYPES:

                self.files.append(p)

        self.files.sort()
        self.dirs.sort(key=lambda x:x.name)

    def playlist(self):
        queue = [self]
        tracks = []
        while len(queue) > 0:
            f = queue.pop(0)
            tracks += f.files
            queue += f.dirs

        return tracks


class Directory:
    def __init__(self, base_path):
        self.path = base_path
        self.folders = dict()
        self.tracks = dict()
        self._parse()

    def _parse(self):
        queue = [Folder("base", self.path, "base")]
        self.folders[queue[0].fid] = queue[0]

        while len(queue) > 0:
            f = queue.pop(0)
            for c in f._parse_children(self.folders, self.tracks):
                queue.append(c)

    def contains(self, fid):
        return fid in self.folders

    def get_folder(self, fid):
        return self.folders.get(fid, None)
"""
