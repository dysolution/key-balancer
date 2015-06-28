import argparse
import os
import sys

from collections import defaultdict
from operator import itemgetter

from exceptions import *
from key import KeyFactory
from track import *


def should_ignore(filename):
    return os.path.splitext(filename)[1].lower() != '.mp3'


def candidates(key_counts):
    candidate_counts = {}
    for name in key_counts.keys():
        candidate_counts[name] = num_candidates(key_counts, name)
    return candidate_counts

def fewest_candidates(key_counts):
    return sorted(candidates(key_counts).iteritems(), key=itemgetter(1))




def main():
    parser = argparse.ArgumentParser(
        description=(
            'Analyze all of the MP3s in a collection and report which '
            'keys are underrepresented; that is, which keys have the '
            'least options to mix out of.'))
    parser.add_argument('base_path')
    parser.add_argument('--bpm', type=int)
    parser.add_argument('--range', type=int)
    parser.add_argument('--verbose', action='store_true',
                        help='list all appropriate tracks')
    args = parser.parse_args()

    keys_found = defaultdict(int)

    for dirpath, dirnames, filenames in os.walk(args.base_path):
        for filename in filenames:
            if should_ignore(filename):
                continue

            full_path = os.path.join(dirpath, filename)
            try:
                track = Track(full_path)
            except IOError:
                continue
            
            try:
                key = KeyFactory.new(track.key)
            except KeyNotFound:
                print "key missing from metadata for {}".format(full_path)
                continue
            
            if args.bpm and args.range:
                try:
                    bpm = track.bpm
                    if not track.tempo_compatible(
                            args.bpm, args.range):
                        continue
                except BpmNotFound:
                    print "no BPM: {}".format(full_path)
                    continue
            keys_found[str(key)] += 1
            if args.verbose:
                print str(track)

    track_count = sum(keys_found.values())
    print "\n==== SUMMARY ===="
    print "* {} tracks found to evaluate.".format(track_count)
    if track_count == 0:
        sys.exit(1)


    mixing_options = fewest_candidates(keys_found)
    fewest = mixing_options[0]
    most = mixing_options[-1]

    if args.bpm and args.range:
        print "* Tempos are between {} bpm and {} bpm.".format(
                args.bpm - args.range, args.bpm + args.range)
    print "* A {:5} track can be mixed into only   {:3} other tracks.".format(
        fewest[0], fewest[1])
    print "* A {:5} track can be mixed into any of {:3} other tracks.".format(
        most[0], most[1])
    print "\n"
    print "\n".join(["{}: {}".format(key[0], key[1])
            for key in mixing_options])


if __name__ == '__main__':
    main()

