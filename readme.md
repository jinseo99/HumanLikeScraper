# HumanLikeScraper

This is a personal project for web/data scraping. 

Key Libraries used:
- Selenium 
- bs4 (BeautifulSoup)

# Description
There are two major parts to this project:
- searching links
- downloading links

To effectively monitor retrieving data from a particular websites with many layer of urls, I have separated the process of searching and downloading contents from the urls. 
Some websites do not allow data access and some disallow robot scraping of their contents.
For educational purposes I have overcame these shortcomings by using Selenium to gain access to websites like a human and optimized the downloads by using threads as multiple workers working on separate webdriver downloads.
