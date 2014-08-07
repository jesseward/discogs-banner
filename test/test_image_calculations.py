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
        self.dimension = calculate_canvas(
                [random.randint(0,50) for r in xrange(50)])

    def test_horizontal_size(self):
        self.assertTrue(self.dimension[0] == 1000)

    def test_vertical_size(self):
        self.assertTrue(self.dimension[1] == 500)

if __name__ == '__main__':
    unittest.main()
