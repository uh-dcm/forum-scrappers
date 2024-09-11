from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from argparse import ArgumentParser

process = CrawlerProcess(get_project_settings())

print("Type keyword to look for:")

key = input()

process.crawl("vauva", start_urls = [f'https://www.vauva.fi/haku?keys={key}&sort&searchpage'])
process.start() 