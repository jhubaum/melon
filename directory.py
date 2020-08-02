import os

FILE_TYPES = ['mp3', 'm4a', 'wma']


class Folder:
    def __init__(self, fid, path, name):
        self.fid = fid
        self.path = path
        self.name = name

        self.dirs = []
        self.files = []

    def _parse_children(self, folders):
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
        self._base_path = base_path
        self._folders = dict()
        self._parse()

    def _parse(self):
        queue = [Folder("base", self._base_path, "base")]
        self._folders[queue[0].fid] = queue[0]

        while len(queue) > 0:
            f = queue.pop(0)
            for c in f._parse_children(self._folders):
                queue.append(c)

    def contains(self, fid):
        return fid in self._folders

    def get_folder(self, fid):
        return self._folders.get(fid, None)
