import unittest
from uh_scrapy.spiders.hevostalli_spider import HevostalliSpider
from fake_response_unittest import mock_response, mock_response_from_file

class hevostalliTest(unittest.TestCase):
    formdata = {"query": 'test',
            "forum": "9"
            }
    def setUp(self):
        self.spider = HevostalliSpider(self.formdata)

    def _test_item_results(self, results, expected_length):
        count = 0
        permalinks = set()
        for item in results:
            self.assertIsNotNone(item['author'])
            self.assertIsNotNone(item['thread'])
            self.assertIsNotNone(item['body'])
            self.assertIsNotNone(item['id'])
            self.assertIsNotNone(item['timestamp'])
            permalinks.add(item['id'])
            count += 1
        self.assertEqual(count, expected_length)
        self.assertEqual(count, expected_length)
        self.assertEqual(len(permalinks), count)

    def test_scrape_thread(self):
        results = self.spider.scrape_thread(mock_response_from_file("scrapy_test_html/hevostalli_thread.html", "http://forum.hevostalli.net/read.php?f=2&i=6866304&t=6866304"))
        self._test_item_results(results, 101)

    def test_parse_threads(self):
        threads = list(self.spider.parse_threads(mock_response_from_file("scrapy_test_html/hevostalli_threads.html", "http://forum.hevostalli.net/list.php?f=1")))
        self.assertEqual(len(threads), 31)
    