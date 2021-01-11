# HumanLikeScraper

This is a personal project for web/data scraping. 

Key Libraries used:
- Selenium 
- bs4 (BeautifulSoup)

# Description
There are two major parts to this project:
- searching links
- downloading links

To effectively monitor retrieving data from a particular website with many layers of urls, I have separated the process of searching and downloading contents from the urls. 
Some websites do allow data access and some disallow robot scraping of their contents.
For educational purposes I have used Selenium to overcome these shortcomings and optimized the downloads by using threads as multiple workers working on separate webdriver downloads.



