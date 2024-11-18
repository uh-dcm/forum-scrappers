# Description
There are a lot of ready made tools for scraping comments from worldwide popular social media resources, but less so for more locally used communities. This is an application for scraping comment-data from Finnish resources with high user traffic. This application is mainly using Scrapy as its backend - a powerful tool for scraping and processing online content. For the frontend it is using Tkinter - a GUI library for Python.

This tool is attempting to be as simple as possible to use. A simple installation and a simple UI that outputs data in a format ready to plug into an analytical tool like 4CAT.

# Installation

    Download repository

    Install requirements from requirements.txt by running

    ``` 
    pip install -r requirements.txt
    ``` 
    
    from the prject directory.

    Run uniwebscraper.py.

# Use
    It is my hope that the UI is self explanatory, but here is a workflow just in case:

    1) Run uniwebscraper.py

    2) In the window that opens you can choose the domain to scrape

    3) After choosing the domain, additional scraping options will pop up.

    4) Fill out the form and press "Start scraping"

    5) The output will be saved to "/scrapedcontent" folder

# Issues
- Due to limitations of Scrapy it is currently necessary to close the window and restart the program to scrape again.


