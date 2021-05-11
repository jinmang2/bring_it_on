""" references
- https://stackoverflow.com/questions/57119258/how-to-do-click-ove-each-element-found-in-table-tbody-in-selenium-python
- https://stackoverflow.com/questions/49579989/python-selenium-click-a-href-javascript
- https://stackoverflow.com/questions/19200497/python-selenium-webscraping-nosuchelementexception-not-recognized/19200889
- https://pcmc.tistory.com/entry/190320-Bot-Detection-%ED%81%AC%EB%A1%A4%EB%9F%AC-%EC%B0%A8%EB%8B%A8-%ED%81%AC%EB%A1%A4%EB%9F%AC-%EC%9A%B0%ED%9A%8C-4-END
"""

import re
import time
from argparse import ArgumentParser

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, 
    StaleElementReferenceException
)


def read_pages(driver, sec=10):
    results = []
    wait = WebDriverWait(driver, sec)
    songlists = driver.find_elements_by_xpath("//*[@id='pageList']//table/tbody/tr")
    N = len(songlists)
    del songlists
    for i in range(N):
        try:
            # get No. {i+1}
            cRow = wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 f"(//*[@id='pageList']//table/tbody/tr)[{i+1}]"))
            )
            # show song's information tag 3
            linkInCurrentRow = cRow.find_elements_by_xpath(".//td[3]/div/div/a")
            # 0: song's information | 1: listen the music by melon player
            linkInCurrentRow[0].click()
            del cRow, linkInCurrentRow
        except StaleElementReferenceException:
            
        
        # informations
        title = driver.find_element_by_class_name("song_name").text
        try:
            artist = driver.find_element_by_class_name("artist").text
            meta_info = driver.find_element_by_class_name("meta").text.split("\n")
            meta = {slot: value for slot, value in zip(meta_info[::2], meta_info[1::2])}
            lyric = driver.find_element_by_class_name("lyric").text
            persons = driver.find_element_by_class_name("list_person").text.split("\n")
            list_person = {slot: value for slot, value in zip(persons[1::2], persons[::2])}
            results.append({
                "title": title,
                "artist": artist,
                "album": meta.get("앨범", None),
                "release_date": meta.get("발매일", None),
                "genre": meta.get("장르", None),
                "lyric": lyric,
                "lyric_writer": list_person.get("작사", None),
                "song_writer": list_person.get("작곡", None),
                "url": driver.current_url
            })
            del title, artist, meta_info, lyric, list_person
        except NoSuchElementException:
            # unregisterd lyrics
            results.append({
                "title": title,
                "artist": None,
                "album": None,
                "release_date": None,
                "genre": None,
                "lyric": None,
                "lyric_writer": None,
                "song_writer": None,
                "url": driver.current_url
            })
            del title
        driver.back()
    return results
  
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrome_path", type=str, default="C:/workspace/chromedriver")
    parser.add_argument("--artist_name", type=str, default="김광석")
    parser.add_argument("--headless", type=bool, default=True)
    parser.add_argument("--page_count", type=int, default=0)
    parser.add_argument("--sleep_time", type=int, default=10)
    args = parger.parse_args()
    
    N = 50
    page_count = args.page_count
    
    op = webdriver.ChromeOptions()
    if args.headless:
        op.add_argument("headless")
        
    results = []
    while True:
        try:
            with webdriver.Chrome(chrome_path, options=op) as driver:
                # Song search page
                website = "https://www.melon.com/search/song/index.htm?q={}&section=artist&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&ipath=srch_form"
                driver.get(website.format(args.artist_name))
                
                total_songs = driver.find_element_by_class_name("serch_totcnt").text
                total_songs = int(re.sub("[^0-9]", "", total_songs))
                
                # checkpoint
                driver.execute_script(f"pageObj.sendPage('{1 + N * page_count}')")
                results.extend(read_pages(driver))
                
                page_count += 1
        except StaleElementReferenceException:
            time.sleep(args.sleep_time)
            continue
            
        if N * page_count >= total_songs:
            break
                
                
                
                
                
                
                
                
                
