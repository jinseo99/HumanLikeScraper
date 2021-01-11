"""
do not use with download_all_links
"""

import threading
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
class searchLinks:
    def __init__(self, lock, archive_path, used_path, main_url, search_url):
        self._lock = lock
        self.archive_path = archive_path
        self.used_path = used_path
        self.main_url = main_url
        self.search_url = search_url
        self.ind = 1
    def savePageSource(self, results):
        used_list = []
        with open(self.used_path, 'r') as tf:
            used_list = tf.read().split('$')
            try:
                used_list.remove("")
            except:
                pass

            for item in results:
                link = item.find('a')
                link = link.get('href')
                url = self.main_url +link
                if url not in used_list:
                    self.saveSource(url)

    def saveSource(self, url):
        with open(self.archive_path, 'a') as tf:
            tf.write("%s$"%url)

    def search(self, driver, worker_id):
        url = ""
        while True:
            with self._lock:
                url = self.search_url + str(self.ind)+'.html'
                #print(url)
                self.ind = self.ind+1

            driver.get(url)
            time.sleep(1)
            page = driver.page_source
            content = BeautifulSoup(page, "html.parser")
            try:
                results = content.find("div", class_="gallery-content")
                if not results.contents:
                    raise Exception
                print(f"worker {worker_id} retrieved {url}")
                self.savePageSource(results, worker_id)

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
    folder = 'text/'
    archive_path = folder+"YacLinkArchive.txt"
    used_path = folder+"YacTitleUsed.txt"
    search_url = ''
    main_url = ''
    sl = searchLinks(lock, archive_path, used_path, main_url, search_url)

    number_of_workers = 5
    for worker_id in range(number_of_workers):
        print(f"{worker_id}, here")

        scraper = worker(webdriver.Chrome(executable_path=chromedriver, options=chrome_options), worker_id, sl)
        scraper.start()
