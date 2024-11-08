from scrapy.http import Request, Response
import requests

import os

from scrapy.http import HtmlResponse

def mock_response_from_file(file_path, url):
    """
    Create a Scrapy fake HTTP response from a HTML file

    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.

    returns: A scrapy HTTP response which can be used for unittesting.
    """

    with open(file_path, 'r', encoding='utf-8') as f:
        body = f.read()
    return HtmlResponse(url=url, body=body, encoding='utf-8')


def mock_response(url):
    """
    Create a mock HTTP response from a URL

    @param url: The URL of the response.

    returns: A scrapy HTTP response which can be used for unittesting.
    """
    request = Request(url)
    response = Response(url=url,
        request=request,
        body=requests.get(url))
    return response
