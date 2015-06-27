from mutagen import mp3


class ArtistNotFound(AttributeError):
    pass


class KeyNotFound(AttributeError):
    pass


class BpmNotFound(AttributeError):
    pass


class Track(object):
    def __init__(self, full_path):
        self.obj = mp3.MP3(full_path)

    def __str__(self):
        try:
            key = self.key
        except KeyNotFound:
            key = 'none'
        return "{:5} {:>3}bpm {} - {}".format(
                key, self.bpm, self.artist, self.title)

    @property
    def key(self):
        return get_key(self.obj)

    @property
    def bpm(self):
        return get_bpm(self.obj)

    def tempo_compatible(self, existing_bpm, bpm_range):
        upper = existing_bpm + bpm_range
        lower = existing_bpm - bpm_range
        return lower <= self.bpm <= upper

    @property
    def title(self):
        return str(self.obj['TIT2'])

    @property
    def artist(self):
        try:
            return str(self.obj['TPE1'])
        except KeyError:
            return ArtistNotFound


def get_bpm(track):
    try:
        return int(round(float(str(track['TBPM']))))
    except KeyError:
        raise BpmNotFound


def get_key(track):
    try:
        return str(track['TKEY'])
    except KeyError:
        raise KeyNotFound
