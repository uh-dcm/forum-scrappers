import unittest
from uh_scrapy.spiders.hs_spider import HSSpider
from tests.fake_response_unittest import mock_response, mock_response_from_file
from uh_scrapy.items import PostItem

class HSSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = HSSpider()


    def _test_item_results(self, results, expected_length):
        count = 0
        permalinks = set()
        for item in results:
            if isinstance(item, PostItem):
                self.assertIsNotNone(item['author'])
                self.assertIsNotNone(item['thread'])
                self.assertIsNotNone(item['body'])
                self.assertIsNotNone(item['id'])
                self.assertIsNotNone(item['timestamp'])
                permalinks.add(item['id'])
                count += 1
        self.assertEqual(count, expected_length)
        self.assertEqual(len(permalinks), count)

    def test_scrape_thread(self):
        results = self.spider.scrape_thread(mock_response_from_file("tests/assets/hs_mock_thread.html", "https://www.hs.fi/api/commenting/hs/articles/2000010898802/comments"))
        self._test_item_results(results, 3)

    def test_parse_threads(self):
        threads = list(self.spider.parse_threads(mock_response_from_file("tests/assets/hs_mock_threads.html", 'https://www.hs.fi/api/search/peruna/kaikki/whenever/new/0/50/0/1765566540655/keyword/')))
        self.assertEqual(len(threads), 51)
    
    