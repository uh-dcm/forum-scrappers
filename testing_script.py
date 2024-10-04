import unittest
from unittest.mock import patch
from uniwebscraper import Search
import constants as ct

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
        
    




if __name__ == "__main__":
    unittest.main()

