import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# 출처 : https://soyoung-new-challenge.tistory.com/22
# 수정 : github.com/jinmang2

#다나와 상품코드 크롤링
def getPcode(page, product):
    pCodeList = []
    for i in range(1,page+1):
        headers = {
               "Referer" : "http://prod.danawa.com/",
               "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
                }

        params = {"page" : page, "listCategoryCode" : 206, "categoryCode" : 206, "physicsCate1":72, 
                  "physicsCate2":73,"physicsCate3":0, "physicsCate4":0, "viewMethod": "LIST", "sortMethod":"BoardCount",
                  "listCount":30, "group": 10, "depth": 2, "brandName":"","makerName":"","searchOptionName":"",
                  "sDiscountProductRate":0, "sInitialPriceDisplay":"N", 
                  "sPowerLinkKeyword":product, "oCurrentCategoryCode":"a:2:{i:1;i:144;i:2;i:206;}", 
                  "innerSearchKeyword":"",
                  "listPackageType":1, "categoryMappingCode":176, "priceUnit":0, "priceUnitValue":0, "priceUnitClass":"",
                  "cmRecommendSort":"N", "cmRecommendSortDefault":"N", "bundleImagePreview":"N", "nPackageLimit":5, 
                  "nPriceUnit":0, "isDpgZoneUICategory": "N", "sProductListApi":"search","priceRangeMinPrice":"","priceRangeMaxPrice":"",
                 "btnAllOptUse":"false"}

        res = requests.post("http://prod.danawa.com/list/ajax/getProductList.ajax.php", headers = headers, data=params)
        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.findAll("a", attrs = {"name":"productName"})
        
        for i in range(len(a)):
            pCodeList.append(a[i]['href'][35:-12])
        
    return pCodeList

#다나와 리뷰 크롤링
def danawaCraw(pcode, page):
    reviewlist = []
    for idx in range(1,page+1):
        headers = {"Referer" : "http://prod.danawa.com/info/?pcode=2703774&cate=102206", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
        params = {"t" : 0.3180507575057596, "prodCode" : pcode, "page" : idx, "limit":10, "score":0,"usefullScore":"Y", "_":1550639162598}

        res = requests.get("http://prod.danawa.com/info/dpg/ajax/companyProductReview.ajax.php?t=0.3180507575057596&prodCode=2703774&page=1&limit=10&score=0&sortType=&usefullScore=Y&_=1550639162598", headers = headers, params = params)
        soup = BeautifulSoup(res.text, "html.parser")
        li = soup.find_all('li', class_="danawa-prodBlog-companyReview-clazz-more")
        res = {}
        for i in li:
            name   = i.find('span', class_='name').text
            date   = i.find('span', class_='date').text
            mall   = i.find('span', class_='mall').text
            star   = i.find('span', class_='star_mask').text
            review = i.find('div', class_='atc').text
            res    = {'pcode':pcode, 'name':name, 'date':date, 'mall':mall, 'star':star, 'review':review}
            reviewlist.append(res)
    return reviewlist

def is_yes_or_no(s):
    def is_yes(s):
        if s.upper() in ['Y', 'YES']: return True
        else: False
    def is_no(s):
        if s.upper() in ['N', 'NO']: return True
        else: False
    yes, no = is_yes(s), is_no(s)
    if not (yes | no):
        return None
    else:
        return yes, no

def main():
    # input 받기
    while True:
        print('***-----------------------------------------------------------------***')
        product   = input('어떤 상품의 리뷰를 얻어올지 입력해주세요.')
        prod_page = input('상품 코드를 몇 개 가져올지 입력해주세요. (상품갯수=입력값*30)')
        page      = input('리뷰를 몇 페이지를 볼지 입력해주세요. (리뷰페이지수=입력값*10')
        predict_time = prod_page * page
        while True:
            try:
                yes, no = is_yes_or_no(input('이 작업은 {:.2f}초만큼의 시간이 소요될 것 같습니다. 진행하시겠습니까? (Y/N)'.format(predict_time)))
            except:
                print('잘못된 값을 입력하셨습니다. 다시 입력해주세요. (Y/N)')
                continue
            break
        if no:
            while True:
                try:
                    yes, no = is_yes_or_no(input('재입력하시겠습니까? (Y/N)'))
                except:
                    print('잘못된 값을 입력하셨습니다. 다시 입력해주세요. (Y/N)')
                    continue
                break
            if yes:
                return None
    
    TotalReview = {'product':[], 'pcode':[], 'name':[], 'date':[], 'mall':[], 'star':[], 'review':[]}
    pCodeList = getPcode(prod_page, product) # 30 * prod_page
    with tqdm(total=30*prod_page*10*page) as t:
        for p in tqdm(pCodeList):
            reviewdict = danawaCraw(p, page) # 10 * page
            for item in tqdm(reviewdict):
                for key, value in item.items():
                    TotalReview['product'].append(product)
                    TotalReview[key].append(value)
                t.update()
    return None

if __name__ == '__main__':
    main()
