from datetime import datetime
from typing import Iterable
import scrapy
from pathlib import Path
import pandas as pd


class YleSpider(scrapy.Spider):
    name= 'yle'

    
    def parse(self, response):
        print()