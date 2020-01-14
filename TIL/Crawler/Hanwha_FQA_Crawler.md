# 한화손해보험 FAQ 데이터 크롤러

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from collections import defaultdict
from selenium.common.exceptions import ElementNotVisibleException, ElementClickInterceptedException
# https://stackoverflow.com/questions/41209832/python-nameerror-name-elementnotvisibleexception-is-not-defined-with-selenium

num2id = {
    1: 'join',
    2: 'product',
    3: 'charge',
    4: 'info',
    5: 'loan',
    6: 'homepage'
}

def crawl_faq_data_from_Hanwha(
        DriverPath, 
        HanwhaFAQ='https://www.hwgeneralins.com/consumer/faq/list.do'):
    driver = webdriver.Chrome(DriverPath)
    driver.get(HanwhaFAQ)
    # 보함가입/보험상품/보험금청구/계약정보/대출/홈페이지
    result = defaultdict(dict) # 결과를 저장할 자료구조 생성
    for BtnNum in range(1, 7):
        MainXPATH = "//div[@class='tab_type1']/ul/li[position()={}]".format(BtnNum)
        driver.find_element(By.XPATH, MainXPATH).click()
        # 세부항목이 몇 개인지 받아오기 위해 정보 수집
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tap_type1 = soup.find('div', {'class': 'tab_type1'}) # Find tab_type1
        sub_topics = tap_type1.find('ul', {'id': num2id[BtnNum]}).find_all('a')
        numSubContents = len(sub_topics)
        sub_names = [tag.text for tag in sub_topics]
        # 세부항목 버튼 클릭
        for SubBtnNum in range(1, numSubContents): # 전체는 패스
            try:
                driver.find_element(By.XPATH, 
                            MainXPATH + "/ul/li[position()={}]".format(SubBtnNum+1)).click()
            except ElementClickInterceptedException as e:
                driver.find_element(By.XPATH, 
                            MainXPATH + "/ul/li[position()={}]".format(SubBtnNum)).click()
                driver.find_element(By.XPATH, 
                            MainXPATH + "/ul/li[position()={}]".format(SubBtnNum+1)).click()
            # 질문 페이지가 몇 개인지 받아오기
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            NumPages = len(soup.find('div', {'class': 'paging', 'id': 'pageDiv'}).find_all('li'))
            print(NumPages)
            res = []
            for page in range(NumPages):
                # page button click
                driver.find_element(By.XPATH,
                        "//div[@id='pageDiv']/ul/li[position()={}]/a".format(page+1)).click()
                # 해당 페이지의 질문의 개수 받아오기
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                NumQuestions = len(soup.find('ul', {'class': 'board_qna'}).find_all('h3'))
                print('\t', NumQuestions)
                for QBtnNum in range(NumQuestions):
                    
                    driver.find_element(By.XPATH,
                                "//div[@id='faqListDiv']/"
                                "ul[@class='board_qna']/"
                                "li[position()={}]/h3/a".format(QBtnNum+1)).click()
                    time.sleep(1)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    # Q와 A 쌍을 저장
                    Q = soup.find_all('h3')[QBtnNum].text
                    A = soup.find_all('div', {'class': 'con'})[QBtnNum].p.text
                    res.append((Q, A))
                time.sleep(5)
            MAIN_TOPIC = num2id[BtnNum]
            SUB_TOPIC = sub_names[SubBtnNum]
            result[MAIN_TOPIC][SUB_TOPIC] = res
    driver.close()
    return result
```
