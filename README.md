# forum-scrappers
## Project plan, loosely:
- 1)Write a scraper for a single forum website(vauva.fi chosen) to develop a framework
- 2)interface the data collection with 4cat
- 3)go down the list on fiam.fi, writing scrapers for each website that has some form of user interaction

## Progress so far:
- Spent half the week reading documentation on various options for web scraping. For now, have settled on scrapy as it seems to be the most easily scaleable and provides good pre-made pipeline for crawling through and handling multiple pages.
- Wrote a web scraper for vauva.fi that allows for use of their search function(limited as it is). It can pull all the pages related to a specific search and create a dataset of posts, authors, parent threads and timestamps. Adding additional fields if necessary is easy.
- NEW: Wrote a scraper for yle.fi that uses yle search system to find all articles relating to particular terms and scrape their comments if existing.

## Issues
- fix error on returning no comments for a search in yle.fi


