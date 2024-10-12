import unittest
from unittest.mock import patch
import constants as ct
'''
class testSearch(unittest.TestCase):

    def setUp(self):
        params = [ct.YLE_CATEGORIES, ct.HS_CATEGORIES, ct.YLE_LANGUAGE]
        query = "searching for new things"
        self.search = Search(params, query)

    @patch('builtins.input', side_effect=['samegiella', 'not', 'samegiella'])
    def test_choose(self, mock_input):
        
        output = self.search.choose(ct.YLE_LANGUAGE)
        expected = ('language=se','samegiella')
        self.assertEqual(output, expected)

        output = self.search.choose(ct.YLE_LANGUAGE)
        expected = ('language=se','samegiella')
        self.assertEqual(output, expected)


    @patch('builtins.input', side_effect=['uutiset', 'kaikki', 'samegiella'])
    def test_fill(self, mock_input):
        self.search.fill()
        expected = [('service=uutiset', 'uutiset'),
                    ('kaikki', 'kaikki'),
                    ('language=se', 'samegiella')]
        self.assertEqual(self.search.body, expected)
        

    @patch('builtins.input', side_effect=['testing a search query'])
    def test_set_search_query(self, mock_input):
        self.search.set_search_query()
        self.assertEqual(self.search.search_query, 'testing a search query')
        
    def test_format_search_query(self):
        output = self.search.format_search_query()
        expected = 'searching%20for%20new%20things'
        self.assertEqual(output, expected)

'''

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from uh_scrapy.spiders.yle_spider import YleSpider
import constants
import pandas as pd

class TestYleSpider(unittest.TestCase):
    
    @patch('scrapy.Request')
    def test_start_requests(self, mock_request):
        search_params = {
            "query": "peruna",
            "category": "uutiset",
            "time": "tanaan",
            "language": "suomi"
        }
        
        spider = YleSpider(search_params)
        spider.start_requests()

        expected_url = spider.query_to_url(spider.count, spider.offset)
        mock_request.assert_called_with(expected_url, callback=spider.parse)

    def test_query_to_url(self):
        search_params = {
            "query": "peruna",
            "category": "uutiset",
            "time": "tanaan",
            "language": "suomi"
        }

        spider = YleSpider(search_params)
        url = spider.query_to_url(50, 0)
        
        expected_url = ('https://yle-fi-search.api.yle.fi/v1/search?app_id=hakuylefi_v2_prod&app_key=4c1422b466ee676e03c4ba9866c0921f'
                        '&limit=50&offset=0&type=article&query=peruna&service=uutiset&time=today&language=fi')
        self.assertEqual(url, expected_url)

    @patch('scrapy.Request')
    def test_parse_with_data(self, mock_request):
        search_params = {
            "query": "test",
            "category": "news",
            "time": "last24h",
            "language": "fi"
        }
        spider = YleSpider(search_params)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'meta': {'count': 100},
            'data': [{'id': 'thread1'}, {'id': 'thread2'}]
        }

        results = list(spider.parse(mock_response))
        self.assertEqual(len(results), 2)  # Two requests for two thread ids
        expected_urls = [
            "https://comments.api.yle.fi/v1/topics/thread1/comments/accepted?app_id=yle-comments-plugin&app_key=sfYZJtStqjcANSKMpSN5VIaIUwwcBB6D",
            "https://comments.api.yle.fi/v1/topics/thread2/comments/accepted?app_id=yle-comments-plugin&app_key=sfYZJtStqjcANSKMpSN5VIaIUwwcBB6D"
        ]
        for i, req in enumerate(results):
            self.assertEqual(req.url, expected_urls[i])
            self.assertEqual(req.callback, spider.scrape_thread)

    @patch('scrapy.Request')
    def test_parse_with_no_data(self, mock_request):
        search_params = {
            "query": "test",
            "category": "news",
            "time": "last24h",
            "language": "fi"
        }
        spider = YleSpider(search_params)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'meta': {'count': 0},
            'data': []
        }

        results = list(spider.parse(mock_response))
        self.assertEqual(len(results), 0)  # No requests should be generated when no data

    def test_scrape_thread(self):
        search_params = {
            "query": "test",
            "category": "news",
            "time": "last24h",
            "language": "fi"
        }
        spider = YleSpider(search_params)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'notifications': None,
            'comments': [{'id': '1', 'content': 'test content'}]
        }

        spider.scrape_thread(mock_response)
        self.assertEqual(len(spider.comments), 1)  # Should add one comment to the list
        self.assertEqual(spider.comments[0]['content'], 'test content')

    def test_make_filename(self):
        search_params = {
            "query": "test",
            "category": "news",
            "time": "last24h",
            "language": "fi"
        }
        spider = YleSpider(search_params)
        dt = datetime(2023, 10, 13, 10, 0, 0)
        with patch('myspider.datetime') as mock_datetime:
            mock_datetime.now.return_value = dt
            filename = spider.make_filename()

        expected_filename = 'scrapedcontent/yle.fi_2023-10-13_10-00-00_querytest_category_news_time_last24h_language_fi'
        self.assertEqual(filename, expected_filename)

    @patch('pandas.DataFrame.to_csv')
    def test_to_4cat_csv(self, mock_to_csv):
        comments = [
            {
                'content': 'test content',
                'author': 'author1',
                'createdAt': '2023-10-13T10:00:00+00:00',
                'id': '1',
                'topicExternalId': 'thread1'
            }
        ]
        filename = 'test_filename.csv'
        spider = YleSpider({})
        spider.to_4cat_csv(comments, filename)

        expected_df = pd.DataFrame({
            'body': ['test content'],
            'author': ['author1'],
            'timestamp': ['2023-10-13 10:00:00'],
            'id': ['1'],
            'thread': ['thread1']
        })
        pd.testing.assert_frame_equal(mock_to_csv.call_args[0][0], expected_df)
        mock_to_csv.assert_called_once_with(filename)

    @patch.object(YleSpider, 'to_4cat_csv')
    @patch.object(YleSpider, 'make_filename', return_value='test_filename.csv')
    def test_closed(self, mock_make_filename, mock_to_4cat_csv):
        search_params = {
            "query": "test",
            "category": "news",
            "time": "last24h",
            "language": "fi"
        }
        spider = YleSpider(search_params)
        spider.comments = [{'id': 1, 'content': 'Test comment'}]
        spider.closed('finished')

        mock_make_filename.assert_called_once()
        mock_to_4cat_csv.assert_called_once_with(spider.comments, 'test_filename.csv')

if __name__ == '__main__':
    unittest.main()

        
    

