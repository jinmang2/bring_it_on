# [부산대학교 한국어 맞춤법 검사기 Crawling으로 접근하기 with `Selenium`](https://speller.cs.pusan.ac.kr/)
```python
from selenium import webdriver
from bs4 import BeautifulSoup
from copy import copy
import time

def spallcheck_using_pusan(reviews, num=10):
    res, is_transform = [], []
    def spallcheck(driver, text):
        checked_text = copy(text)
        driver.find_element_by_name('text1').send_keys(text)
        driver.find_element_by_id('btnCheck').click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        is_valid = soup.find('div', {"class":"divScrollbarStyle", 'id':'divLeft1'})
        if is_valid:
            announceText = soup.find('td', {'id':'pageAnnounce'}).text
            t = is_valid.td
            rule = {f.next.next_sibling : f.span.text for f in t.find_all('font')}
            if announceText:
                for i in range(1, int(announceText.split(' ')[1].split('페이지')[0])):
                    driver.find_element_by_id('nextBtn').click()
                    t = soup.find('div', {"class":"divScrollbarStyle", 'id':'divLeft1'}).td
                    for f in t.find_all('font'):
                        rule[f.next.next_sibling] = f.span.text
            for i,j in rule.items():
                checked_text = checked_text.replace(i, j)     
            transform = True
        else:
            transform = False
        driver.find_element_by_id('btnRenew2').click()
        return checked_text, transform
    driver = webdriver.Chrome('C:/research_persona/Crawler/chromedriver')
    print('---** selenium으로 web에 접근 중 ... 3초 소요됩니다... **---')
    driver.implicitly_wait(3)
    print('Connected. spaller.cs.pusan.ac.kr/에 접속합니다.')
    driver.get('https://speller.cs.pusan.ac.kr/')
    print('text 분석을 실시합니다. 1000개 text마다 결과를 기록합니다.')
    start, semi_start = time.time(), time.time()
    for ix, text in enumerate(reviews):
        if ix % num == 0:
            if time.time() - start >= 60:
                a = (time.time() - start) / 3600
                b = 'hours'
            else:
                a = (time.time() - start) / 60
                b = 'mins'
            print(ix, '\t\tcollapse {:.2f} mins\t\tcumulative time is {:.2f} {:s}'.format(
                (time.time() - semi_start) / 60, a, b))
            semi_start = time.time()
        try:
            checked_text, transform = spallcheck(driver, text)
        except:
            print('Error: 에러 발생!')
            return res, is_transform
        res.append(checked_text)
        is_transform.append(transform)
    driver.close()
    return res, is_transform
```
