import unittest
from uh_scrapy.spiders.kaksplus_spider import KaksplusSpider
from tests.fake_response_unittest import mock_response, mock_response_from_file
from uh_scrapy.items import PostItem

class KaksPlusSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = KaksplusSpider()

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
        results = self.spider.scrape_thread(mock_response_from_file("tests/assets/kaksplus_mock_thread.html", "https://keskustelu.kaksplus.fi/threads/ammattisi-ja-puolue-jota-aeaenestit.2005095/#post-24283128"))
        self._test_item_results(results, 25)

    def test_parse_threads(self):
        threads = list(self.spider.parse_threads(mock_response_from_file("tests/assets/kaksplus_mock_threads.html", "https://keskustelu.kaksplus.fi/keskustelu/haku/1598345/?q=Engineer&o=relevance")))
        self.assertEqual(len(threads), 21)


    
    