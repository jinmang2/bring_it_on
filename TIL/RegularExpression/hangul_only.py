import re

def hangul_only(s):
    nothangul = re.compile('[^ㄱ-ㅎㅏ-ㅣ가-힣]')
    return re.sub(nothangul, '', s)
    
s1 = 'I like 파이썬 programming'
s2 = 'a1가b2나c3다d4라e5마f6바g7사'

hangul_only(s1) # '파이썬'
hangul_only(s2) # '가나다라마바사'
