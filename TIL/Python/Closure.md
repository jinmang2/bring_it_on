# Closure

## Closure란?
- In programming language, 퍼스트클래스 함수를 지원하는 언어의 name binding 기술
- 어떤 함수를 함수 자신이 가지고 있는 환경과 함께 저장한 레코드
- 함수가 가진 프리변수(free variable)를 클로저가 만들어지는 당시의 값과 레퍼런스에 매핑하여 주는 역할을 수행
    - Free Variable in Python
        - 코드블럭 안에서 사용은 되었지만, 그 코드블럭 안에서 정의되지 않은 변수를 의미
- 일반 함수와는 다르게, 자신의 영역 밖에서 호출된 함수의 변수값과 레퍼런스를 복사하고 저장한 뒤, 이 캡처한 값들에 엑세스할 수 있게 도와줌
- 언어가 first-class function이 되어야 만들 수 있음
- java script에서도 큰 역할을 하고 있음
    - js에는 class가 없음. 일부로 구현을 안함
    - js진영: 우리도 OOP(Object Oriented Programming)쓰고 싶어요!
    - oop 대용으로 나온 것이 closure
- python에서는 closure를 쓰실 일이 거의 없음
- OOP로 대부분 해결 가능!

## 뭔소리야;; 코드로 이해!
- case 1.
```python
# -*- coding: utf-8 -*-
def outer_func():         #1
    message = 'Hi'        #3
    def inner_func():     #4
        print(message)    #6
    return inner_func()   #5

outer_func()              #2
```
```
Hi
```
일련의 과정
1. #1에서 정의된 함수 outer_func를 #2에서 호출. outer_func는 어떤 인수도 받지 않음
2. outer_func가 실행된 후, 가장 먼저 하는 것은 message라는 변수에 'Hi'라는 문자열을 할당. #3
3. #4번에서 inner_func를 정의하고 #5번에서 inner_func를 호출하며 동시에 리턴
4. #6에서 message 변수를 참조하여 출력. 여기서 message는 inner_func 안에서 정의되지 않았지만, inner_func 안에서 사용되기 때문에 free variable이라고 부름

- case 2.
```python
# -*- coding: utf-8 -*-
def outer_func():         #1
    message = 'Hi'        #3
    def inner_func():     #4
        print(message)    #6
    return inner_func     #5  <-- 함수를 실행하지 않고 그냥 넘기면?

outer_func()              #2
```
```
None
```

- case 3.
```python
# -*- coding: utf-8 -*-
def outer_func():         #1
    message = 'Hi'        #3
    def inner_func():     #4
        print(message)    #6
    return inner_func     #5

my_func = outer_func()    #2  <-- 리턴값인 inner_func를 변수에 할당
                              # 어떤 값도 출력되지 않는다.
print(my_func)
```
```
<function outer_func.<locals>.inner_func at 0x000002D0C150EEE8>
```

- case 4. 위의 my_func를 이용해 inner_func 함수 호출
```python
my_func()
my_func()
my_func()
```
```
Hi
Hi
Hi
```
이상한데...? outer_func는 #2에서 호출된 이후 종료. 근데 my_func()를 호출했을 때 outer_func의 로컬 변수인 message를 참조

- case 5. 클로저는 도대체 함수의 프리변수를 어디에 저장할까?
```python
# -*- coding: utf-8 -*-

def outer_func():
    message = 'Hi'
    def inner_func():
        print(message)
    return inner_func
    
my_func = outer_func()

print(my_func, end='\n\n')
print(dir(my_func), end='\n\n')
print(type(my_func.__closure__, end='\n\n')
print(my_func.__closure__, end='\n\n')
print(my_func.__closure__[0], end='\n\n')
print(dir(my_func.__closure__[0]), end='\n\n')
print(my_func.__closure__[0].cell_contents)
```
```
<function outer_func.<locals>.inner_func at 0x000002D0C19F19D8>

['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', 
'__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', 
'__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', 
'__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']

<class 'tuple'>

(<cell at 0x000002D0C1A9CA98: str object at 0x000002D0C17007F0>,)

<cell at 0x000002D0C1A9CA98: str object at 0x000002D0C17007F0>

['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', 
'__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', 
'__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'cell_contents']


Hi
```

- case 6. 함수의 파라미터를 사용, 더 재밌는 코드를 만들어보자.
```python
# -*- coding: utf-8 -*-

def outer_func(tag):
    tag = tag
    def inner_func(txt):
        text = txt
        print('<{0}>{1}<{0}>'.format(tag, text))
    return inner_func
    
h1_func = outer_func('h1')
p_func = outer_func('p')

h1_func('h1태그의 안입니다.')
p_func('p태그의 안입니다.')
```
```
<h1>h1태그의 안입니다.<h1>
<p>p태그의 안입니다.<p>
```
### 클로저의 의의?
클로저는 이렇게 하나의 함수로 여러가지의 함수를 간단히 만들어낼 수 있게도 해주며, 기존에 만들어진 함수나 모듈 등을 수정하지 않고도 wrapper 함수를 이용해 커스터마이징할 수 있게 해주는 기특한 녀석.


출처
- [SCHOOL OF WEB, 파이썬-클로저](http://schoolofweb.net/blog/posts/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%81%B4%EB%A1%9C%EC%A0%80-closure/)
- [jinmang2/cs_bootcamp_python](https://github.com/jinmang2/cs_bootcamp_python/blob/master/bootcamp_2%EC%A3%BC%EC%B0%A8%20%EC%A0%95%EB%A6%AC.ipynb)

