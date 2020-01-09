## Link
- https://soyoung-new-challenge.tistory.com/22

## 어떤 역할?
- 상품명을 넣으면 [Danawa](http://www.danawa.com/) 사이트에서 상품명을 검색하여 리뷰를 받아오는 코드
- 수정내역
  - 2019.09.24
    - 아래의 코드에서 리뷰가 있는 태그를 읽어들이지 못하는 에러가 발생. 
    ```python
    def danawaCraw(pcode, page):
      ~~~
      divs = soup.find_all("div", attrs={"style":"display:none"})
      ~~~
    ```
    - 문제 확인
    ```
    (향후 추가)
    ```
    - 때문에 아래의 코드로 수정하여 review가 있는 데이터 수집
    ```python
    def danawaCraw(pcode, page):
      ~~~
      divs = soup.find_all("div", class_="atc") # python에서 class는 예약어
      ~~~
    ```
- 향후 추가 내용
  - 많은 상품명을 받아와야 하기 때문에 중간중간에 `JSON`이나 `XML`, `DataFrame` 형태로 저장하여 기록하는 코드 필요
  - 각 리뷰별 상품에 대한 특성이라든지 이름, 날짜 데이터 등을 받아서 구조체 데이터로 저장할 필요 존재
  
## 코드는?
```python
#다나와 상품코드 크롤링
def getPcode(page, product):
    pCodeList = []
    for i in range(1,page+1):
        print(i,"페이지 입니다")
        headers = {
               "Referer" : "http://prod.danawa.com/",
               "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
                }

        params = {"page" : page, "listCategoryCode" : 206, "categoryCode" : 206, "physicsCate1":72, 
                  "physicsCate2":73,"physicsCate3":0, "physicsCate4":0, "viewMethod": "LIST", "sortMethod":"BoardCount",
                  "listCount":30, "group": 10, "depth": 2, "brandName":"","makerName":"","searchOptionName":"",
                  "sDiscountProductRate":0, "sInitialPriceDisplay":"N", 
                  "sPowerLinkKeyword":product, 
                  "oCurrentCategoryCode":"a:2:{i:1;i:144;i:2;i:206;}", 
                  "innerSearchKeyword":"",
                  "listPackageType":1, "categoryMappingCode":176, "priceUnit":0, "priceUnitValue":0, "priceUnitClass":"",
                  "cmRecommendSort":"N", "cmRecommendSortDefault":"N", "bundleImagePreview":"N", "nPackageLimit":5, 
                  "nPriceUnit":0, "isDpgZoneUICategory": "N", "sProductListApi":"search",
                  "priceRangeMinPrice":"","priceRangeMaxPrice":"",
                 "btnAllOptUse":"false"}

        res = requests.post("http://prod.danawa.com/list/ajax/getProductList.ajax.php", 
                            headers = headers, data=params)
        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.findAll("a", attrs = {"name":"productName"})
        
        for i in range(len(a)):
            pCodeList.append(a[i]['href'][35:-12])
        
    return pCodeList

#다나와 리뷰 크롤링
def danawaCraw(pcode, page):
    reviewlist = []
    for idx in range(1,page+1):
        headers = {"Referer" : "http://prod.danawa.com/info/?pcode=2703774&cate=102206", 
                   "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
        params = {"t" : 0.3180507575057596, 
                  "prodCode" : pcode, 
                  "page" : idx, 
                  "limit":10, 
                  "score":0,
                  "usefullScore":"Y", 
                  "_":1550639162598}

        res = requests.get(
            "http://prod.danawa.com/info/dpg/ajax/companyProductReview.ajax.php?t=0.3180507575057596&prodCode=2703774&page=1&limit=10&score=0&sortType=&usefullScore=Y&_=1550639162598", 
            headers = headers, params = params)
        soup = BeautifulSoup(res.text, "html.parser")
        divs = soup.find_all("div", class_="atc")
        #print(idx,'페이지에서', len(divs),'개의 리뷰 크롤링완료')
        for i in range(len(divs)):
            reviewlist.append(divs[i].text)
    return reviewlist
```
