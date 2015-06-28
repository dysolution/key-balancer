from collections import defaultdict
from operator import itemgetter

from key import MAJOR_KEYS, MINOR_KEYS, KeyFactory


GRAPH_CHAR = '*'


class MusicCollection(list):

    def __init__(self):
        self.count_for = {}
        for key in MINOR_KEYS + MAJOR_KEYS:
            self.count_for[key] = 0

    def __len__(self):
        return sum(self.count_for.values())

    def add_track(self, track):
        self.append(track)
        self.count_for[str(KeyFactory.new(track.key))] += 1

    def suitable_next_track_count(self, key):
        _key = KeyFactory.new(key)
        same = self.count_for[str(KeyFactory.new(key))]
        higher = self.count_for[_key.up_fifth]
        lower = self.count_for[_key.down_fifth]
        relative = self.count_for[_key.relative]
        return same + higher + lower + relative

    @property
    def keys_with_option_counts(self):
        for key, next_track_count in self.sorted_with_next_track_counts:
            if self.count_for[key] > 0:
                candidates = self.suitable_next_track_count(key)
                print "{:>3} {:5} tracks can be mixed into {:>3} other tracks: {}".format(self.count_for[key], key, candidates, GRAPH_CHAR * candidates)

    @property
    def sorted_keys(self):
        return sorted(self.count_for.iteritems(), key=itemgetter(1))

    @property
    def sorted_with_next_track_counts(self):
        return sorted([(key, self.suitable_next_track_count(key)) for key, count in self.sorted_keys], key=itemgetter(1))
