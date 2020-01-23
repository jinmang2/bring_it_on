# `functools.partial`
- `sklearn.feature_extraction.text.CountVectorizer` 소스 코드 분석 중 만난 `partial`에 대해 공부

### Partial이란?
- 하나 이상의 인수가 이미 채워진 함수의 새 버전을 만들기 위해 사용된다.
- 함수의 새 버전은 그 자체를 기술하고 있다.
```python
def power(base, exponent):
    return base ** exponent
    
def square(base):
    return power(base, 2)
    
def cube(base):
    return power(base, 3)
    
# 위 같이 반복적인 함수 코드를 작성하는 것은 짜증나기 이루 말할 수 없다.
# 이런 일을 할 때 partial을 이용

from functools import partial

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

def test_partials():
    assert square(2) == 4
    assert cube(2) == 8
    
# 부분함수에 대한 속성은 아래와 같이 기술할 수 있다.
def test_partial_docs():
    assert square.keywords == {'exponent':2}
    assert square.func == power
    
    assert cube.keywords == {'exponent':3}
    assert cube.func == power
```

출처: https://hamait.tistory.com/823
