"""
do not use with download_all_links
"""

import threading
from bs4 import BeautifulSoup
from selenium import webdriver
import time

class searchLinks:
    def __init__(self, lock, link_path, title_path, main_url, search_url):
        self._lock = lock
        self.link_path = link_path
        self.title_path = title_path
        self.main_url = main_url
        self.search_url = search_url
        self.ind = 1

    def getRawInfo(self, results):
        for item in results:
            link = item.find('a').get('href')
            url = self.main_url +link
            title =item.find('h1').text
            with self._lock:
                self.saveLink(url)
                self.saveTitle(title)
    
    def saveTitle(self, item):
        with open(self.title_path, 'a') as tf:
            tf.write(f"{item}$")

    def saveLink(self, item):
        with open(self.link_path, 'a') as tf:
            tf.write(f"{item}$")
    
    def retrieve(self, driver, url):
        driver.get(url)
        time.sleep(1)
        page = driver.page_source
        content = BeautifulSoup(page, "html.parser")
        return content

    def search(self, driver, worker_id):
        url = ""
        while True:
            with self._lock:
                url = self.search_url + str(self.ind)+'.html'
                self.ind = self.ind+1
            
            content = self.retrieve(driver, url)

            try:
                results = content.find("div", class_="gallery-content")
                if not results.contents:
                    raise Exception
                if len(results) < 25:
                    content = self.retrieve(driver, url)
                    results = content.find("div", class_="gallery-content")
                    print("check link below updated:", len(results))

                print(f"worker {worker_id} retrieved {url}")
                self.getRawInfo(results)

            except Exception as e:
                print(str(e))
                print(f"worker {worker_id} not retrieved {url}")
                return




class worker(threading.Thread):
    def __init__(self, driver, worker_id, shared_sl):
        threading.Thread.__init__(self)
        self.sl = shared_sl
        self.driver = driver
        self.worker_id = worker_id
    def run(self):
        self.sl.search(self.driver, self.worker_id)
        self.driver.close()


if __name__ == '__main__':

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    prefs = {'download.default_directory' : '/YacStorage'}
    chrome_options.add_experimental_option('prefs', prefs)
    chromedriver="/chromedriver"

    lock = threading.Lock()
    folder = 'text/website/'
    link_path = folder+"link.txt"
    title_path = folder+"title.txt"
    search_url = ''
    main_url = ''
    sl = searchLinks(lock, link_path, title_path, main_url, search_url)

    number_of_workers = 5
    for worker_id in range(number_of_workers):
        print(f"{worker_id}, here")

        scraper = worker(webdriver.Chrome(executable_path=chromedriver, options=chrome_options), worker_id, sl)
        scraper.start()
