from bs4 import BeautifulSoup
from selenium import webdriver
import time

test_url = ''
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
prefs = {'download.default_directory' : '/YacStorage'}
chrome_options.add_experimental_option('prefs', prefs)
chromedriver="/chromedriver"

driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)
driver.get(test_url)

time.sleep(1)
page = driver.page_source
content = BeautifulSoup(page, "html.parser")


main_url = ''

results = content.find("div", class_="gallery-content")

url_list = []
print(len(results))

for item in results:
    link = item.find('a')
    link = link.get('href')
    url_list.append(main_url +link)

print(len(url_list))
