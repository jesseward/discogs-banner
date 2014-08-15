import unittest
import random

from discogs_banner.canvas_tools import normalize_thumbs, calculate_canvas

class TestThumbRestrictions(unittest.TestCase):

    def setUp(self):
      self.thumbs = normalize_thumbs(
              [random.randint(0,150) for r in xrange(150)])

    def test_thumb_length(self):
      self.assertTrue(len(self.thumbs) == 119)

class TestCanvasSizes(unittest.TestCase):

    def setUp(self):
        ''' 16x9, 4x3, 2x1 '''

        self.twobyone = calculate_canvas(
                [random.randint(0,50) for r in xrange(50)], aspect='2x1')
        self.fourbythree = calculate_canvas(
                [random.randint(0,50) for r in xrange(50)], aspect='4x3')
        self.sixteenbynine = calculate_canvas(
                [random.randint(0,50) for r in xrange(50)], aspect='16x9')

    def test_horizontal_size_2x1(self):
        self.assertTrue(self.twobyone[0] == 1000)

    def test_vertical_size_2x1(self):
        self.assertTrue(self.twobyone[1] == 500)

    def test_horizontal_size_4x3(self):
        self.assertTrue(self.fourbythree[0] == 800)

    def test_vertical_size_4x3(self):
        self.assertTrue(self.fourbythree[1] == 600)

    def test_horizontal_size_16x9(self):
        self.assertTrue(self.sixteenbynine[0] == 900)

    def test_vertical_size_16x9(self):
        self.assertTrue(self.sixteenbynine[1] == 500)

if __name__ == '__main__':
    unittest.main()
