from builtins import object

class MusicQueue(object):
    _queue = []
    _index = None
    _loop = False

    def __init__(self):
        pass

    def __len__(self):
        return len(self._queue)

    def enqueue(self, track):
        if len(self._queue) == 0:
            self._index = 0
        self._queue.append(track)

    def next(self):
        if len(self._queue) >= self._index + 1:
            self._index += 1
            return self._queue[self._index]
        elif self._loop:
            self._index = 0
            return self._queue[self._index]
        return None

    def prev(self):
        if self._index <= 0 and self._loop:
            self._index = len(self._queue) + 1
        if self._index is not None:
            self._index -= 1
            return self._queue[self._index]
        else:
            return None

    def current(self):
        return self._queue[self._index]

    def clear(self):
        self._index = None
        self._queue = []
