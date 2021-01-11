"""

to download: archive + (start - downloaded)

next round of archive use any of ($) < > # % { } | \ ^ ~ [ ] 
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import threading
import time

class downloadLinks:
    def __init__(self, lock, archive_path, used_path, started_path, downloaded_path, invalid_path):
        self._lock = lock
        self.archive_path = archive_path
        self.used_path = used_path
        self.started_path = started_path
        self.downloaded_path = downloaded_path
        self.invalid_path = invalid_path

    def getSource(self):
        viable_source =""
        source_list = []
        with open(self.archive_path, 'r') as tf:
            source_list = tf.read().split("$")
            try:
                source_list.remove("")
            except:
                pass
            if not source_list:
                return None
                
        viable_source = source_list[0]
        source_list.remove(viable_source)

        with open(self.archive_path, 'w') as tf:
            for item in source_list:
                tf.write(f"{item}$")

        with open(self.used_path, 'a') as tf:
            tf.write("%s$" % viable_source)
        
        return viable_source

    def trackDownload(self, filepath, url):
        with open(filepath, 'a') as tf:
            tf.write("%s$" % url)
    
    def checkUnDownloaded(self):
        downloaded_list = []
        started_list = []
        try:
            with open(self.started_path, 'r+') as tf:
                started_list = tf.read().split('$')
                try:
                    started_list.remove("")
                except:
                    pass
                tf.truncate(0) 
            with open(self.downloaded_path, 'r+') as tf:
                downloaded_list = tf.read().split('$')
                try:
                    downloaded_list.remove("")
                except:
                    pass
                tf.truncate(0)
        except:
            return
            
        not_downloaded = list(set(started_list)-set(downloaded_list))

        if not not_downloaded:
            return
        else:

            with open(self.archive_path, 'a') as tf:
                for item in not_downloaded:
                    tf.write(f"{item}$")

            used_list = []
            with open(self.used_path, 'r') as tf:
                used_list = tf.read().split('$')
                try:
                    used_list.remove("")
                except:
                    pass
            new_list = list(set(used_list)-set(not_downloaded))
            with open(self.used_path, 'w') as tf:
                for item in new_list:
                    tf.write(f"{item}$")


    def download(self, driver, worker_id):
        with self._lock:
            self.checkUnDownloaded()
        while True:
            url = ""
            with self._lock: 
                url = self.getSource()
                if url is None:
                    return
            
            driver.get(url)
            time.sleep(1)
            try:
                element = driver.find_element_by_xpath("//a[@id='dl-button']")
                driver.execute_script("arguments[0].click();", element)
                print(f"worker {worker_id} started download {url}")
            except:
                print(f"worker {worker_id} got invalid {url}")
                self.trackDownload(self.invalid_path, url)
                continue
            with self._lock:
                self.trackDownload(self.started_path, url)

            
            start_time = time.time()
            while True:
                try:
                    if time.time() - start_time > 30*60:
                        print(f"worker {worker_id} timeout download {url}")
                        break

                    time.sleep(5)
                    page = driver.page_source
                    content = BeautifulSoup(page, "html.parser")
                    results = content.find("div", id="progressbar")
                    value = results.get('aria-valuenow')
                    if int(value) == 100:
                        print(f"worker {worker_id} finished download {url}")
                        with self._lock:
                            self.trackDownload(self.downloaded_path, url)
                        break
                except:
                    time.sleep(5)
                    continue



class worker(threading.Thread):
    def __init__(self, driver, worker_id, shared_dl):
        threading.Thread.__init__(self)
        self.dl = shared_dl
        self.driver = driver
        self.worker_id = worker_id
    def run(self):
        self.dl.download(self.driver, self.worker_id)
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
    used_path = folder+"YacLinkUsed.txt"
    started_path = folder+"YacStarted.txt"
    downloaded_path = folder+"YacDownloaded.txt"
    invalid_path = folder+ "Invalid.txt"

    dl = downloadLinks(lock, archive_path, used_path, started_path, downloaded_path, invalid_path)
    number_of_workers = 5
    for worker_id in range(number_of_workers):
        print(f"{worker_id}, here")

        scraper = worker(webdriver.Chrome(executable_path=chromedriver, options=chrome_options), worker_id, dl)
        scraper.start()
