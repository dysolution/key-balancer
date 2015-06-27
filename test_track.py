import unittest

from track import *

class TestTrack(unittest.TestCase):

    def test_bpm(self):
        self.assertEqual(get_bpm({'TBPM': '100'}), 100)
        self.assertEqual(get_bpm({'TBPM': '0.0'}), 0)

    def test_key(self):
        self.assertEqual(get_key({'TKEY': 'Amin'}), 'Amin')
        self.assertEqual(get_key({'TKEY': ''}), '')
