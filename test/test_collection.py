import unittest
import logging

from discogs_banner.api_tools import fetch_collection

logger = logging.getLogger(__name__)
logging.disable(logging.CRITICAL)

class TestDiscogsCollectionValidUser(unittest.TestCase):

    def setUp(self):
      self.collection = fetch_collection('jim')

    def test_response(self):
      self.assertTrue(len(self.collection) == 3)

    def test_release_id(self):
      self.assertTrue(self.collection[0][0] == 32251)

    def test_resource_url(self):
      self.assertTrue(self.collection[0][1] == 
          'http://api.discogs.com/releases/32251')

    def test_thumb_url(self):
      self.assertTrue(self.collection[0][2] == 
          'http://api.discogs.com/image/R-150-32251-1217277145.jpeg')

class TestDiscogsCollectionInvalidUser(unittest.TestCase):

    def setUp(self):
      self.collection = fetch_collection('invalid-discogs-username')

    def test_response(self):
      self.assertTrue(len(self.collection) == 0)

if __name__ == '__main__':
    unittest.main()
