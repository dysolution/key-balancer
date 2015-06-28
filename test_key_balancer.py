import unittest

from key import *
from music_collection import *


class TestKeyFactory(unittest.TestCase):
    def test_good_abbreviations(self):
        a_min = KeyFactory.new('Amin')
        a_m = KeyFactory.new('Am')
        gsharp_min = KeyFactory.new('G#min')
        gsharp_m = KeyFactory.new('G#m')
        self.assertEqual(str(a_min), str(a_m))
        self.assertEqual(str(gsharp_min), str(gsharp_m))

    def test_bad_names(self):
        self.assertIsInstance(KeyFactory.new(''), NullKey)
        self.assertIsInstance(KeyFactory.new('invalid'), NullKey)
        self.assertIsInstance(KeyFactory.new('Gflat'), NullKey)


class TestKey(unittest.TestCase):

    def test_can_be_followed_with(self):
        k1 =  Key('Amin')
        self.assertTrue(k1.can_be_followed_with(Key('Emin')))
        self.assertTrue(k1.can_be_followed_with(Key('Dmin')))
        self.assertTrue(k1.can_be_followed_with(Key('Cmaj')))
        self.assertTrue(k1.can_be_followed_with(Key('Amin')))

        self.assertFalse(k1.can_be_followed_with(Key('Fmin')))
        self.assertFalse(k1.can_be_followed_with(Key('D#min')))
        self.assertFalse(k1.can_be_followed_with(Key('Cmin')))
    
    def test_up_fifth(self):
        self.assertEqual(Key('Amin').up_fifth, 'Emin')
        self.assertEqual(Key('Dmin').up_fifth, 'Amin')
        self.assertEqual(Key('C#min').up_fifth, 'G#min')
        self.assertEqual(Key('G#min').up_fifth, 'D#min')

    def test_down_fifth(self):
        self.assertEqual(Key('Dmin').down_fifth, 'Gmin')
        self.assertEqual(Key('G#min').down_fifth, 'C#min')
        self.assertEqual(Key('A#min').down_fifth, 'D#min')

    def test_relative(self):
        self.assertEqual(Key('Dmin').relative, 'Fmaj')
        self.assertEqual(Key('Cmaj').relative, 'Amin')

    def test_quality(self):
        self.assertEqual(Key('Dmin').quality, 'minor')
        self.assertEqual(Key('Emaj').quality, 'major')
        with self.assertRaises(AttributeError):
            Key('invalid').quality


@unittest.skip('file IO')
class TestKeyBalancer(unittest.TestCase):
    def setUp(self):
        self.keys_found = {'Cmin': 5, 'Gmin': 2,
                           'Fmin': 4, 'A#min': 6}
        self.mp3 = Track(r'c:\temp\foo.mp3')

    def test_num_candidates(self):
        kf = self.keys_found
        self.assertEqual(num_candidates(kf, 'Cmin'), 10)
        self.assertEqual(num_candidates(kf, 'Gmin'), 6)
        self.assertEqual(num_candidates(kf, 'Fmin'), 14)
        self.assertEqual(num_candidates(kf, 'A#min'), 9)

    def test_candidates(self):
        self.assertEqual(candidates(self.keys_found)['Gmin'], 6)
        self.assertEqual(candidates(self.keys_found)['Cmin'], 10)
        self.assertEqual(candidates(self.keys_found)['A#min'], 9)
        self.assertEqual(candidates(self.keys_found)['Fmin'], 14)

    def test_fewest_candidates(self):
        self.assertEqual(fewest_candidates(self.keys_found),
                [('Gmin', 6), ('A#min', 9), ('Cmin', 10), ('Fmin', 14)])

    def test_key(self):
        self.assertEqual(self.mp3.key, 'Cmin')

    def test_bpm(self):
        self.assertEqual(self.mp3.bpm, 124)

    def test_bpm_is_ok(self):
        self.assertEqual(self.mp3.bpm, 124)
        self.assertTrue(self.mp3.tempo_compatible(122, 2))
        self.assertTrue(self.mp3.tempo_compatible(125, 3))
        self.assertFalse(self.mp3.tempo_compatible(120, 2))


class FakeTrack(object):
    @property
    def key(self):
        return 'Amin'


class TestMusicCollection(unittest.TestCase):
    def setUp(self):
        self.mc = MusicCollection()

    def tearDown(self):
        self.mc = None

    def test_add_track(self):
        self.assertEqual(len(self.mc), 0)
        self.assertEqual(self.mc.count_for['Amin'], 0)

        self.mc.add_track(FakeTrack())
        self.assertEqual(len(self.mc), 1)
        self.assertEqual(self.mc.count_for['Amin'], 1)
