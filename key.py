MINOR_KEYS = ['G#min', 'D#min', 'A#min', 'Fmin', 'Cmin', 'Gmin',
              'Dmin', 'Amin', 'Emin', 'Bmin', 'F#min', 'C#min']

MAJOR_KEYS = ['Bmaj', 'F#maj', 'C#maj', 'G#maj', 'D#maj', 'A#maj',
              'Fmaj', 'Cmaj', 'Gmaj', 'Dmaj', 'Amaj', 'Emaj']

class NullKey(object):

    def __str__(self):
        return 'None'

    def up_fifth(self):
        return self

    def down_fifth(self):
        return self

    def relative(self):
        return self


class Key(object):
    def __init__(self, key):
        self.key = key

    def __unicode__(self):
        return unicode(self.key)

    def __str__(self):
        return self.__unicode__()

    @property
    def quality(self):
        if self.key.lower().endswith('maj'):
            return 'major'
        elif self.key.lower().endswith('min'):
            return 'minor'
        else:
            raise AttributeError(
                "couldn't determine key quality: {}".format(self.key))

    @property
    def up_fifth(self):
        return self._keys[self._key_num + 1 if self._key_num < 11 else 0]

    @property
    def down_fifth(self):
        return self._keys[self._key_num - 1 if self._key_num > 0 else 11]

    @property
    def relative(self):
        return self._relatives[self._keys.index(self.key)]

    # private
    @property
    def _keys(self):
        if self.quality == 'major':
            return MAJOR_KEYS
        elif self.quality == 'minor':
            return MINOR_KEYS

    @property
    def _relatives(self):
        if self.quality == 'major':
            return MINOR_KEYS
        elif self.quality == 'minor':
            return MAJOR_KEYS

    @property
    def _key_num(self):
        return self._keys.index(self.key)

    @property
    def _valid(self):
        return self.key in self._keys


class KeyFactory(object):

    @classmethod
    def new(self, key):
        if key == '':
            return NullKey()

        if self._is_abbreviation(key):
            for full in MINOR_KEYS:
                if full.startswith(key):
                    return Key(full)
            return NullKey()

        if self._is_valid(key):
            return Key(key)
        else:
            return NullKey()

    # private
    @classmethod
    def _is_abbreviation(self, key):
        return len(key) < 4

    @classmethod
    def _is_valid(self, key):
        return key in MINOR_KEYS + MAJOR_KEYS

