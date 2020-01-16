# First Class Function

### 퍼스트 클래스 함수란?
- 프로그래밍 언어가 함수(function)을 first-class citizen으로 취급하는 것
- 쉽게 아래의 조건을 만족시키면 first-class function이라고 명명함
  - 첫 째, 함수를 argument(인자)로 전달할 수 있는가
  - 둘 째, 함수를 varirable(변수)로 전달할 수 있는가
  - 셋 째, return(반환값)으로 함수를 사용할 수 있는가

### 어떤 언어들이 first-class function을 만족할까?
- python은 이를 지원
- c언어는 포인터를 넘겨서 사용
- js는 지원을 함

### 뭔 소리지;; 코드로 보자!
#### 1. 함수를 argument로 전달할 수 있는가
```python
def f(a, b):
    return a + b
    
# 함수를 argument로 calling
# 이게 먹힌다는 얘기는 함수를 인자로 전달할 수 있다는 얘기

def g(func, a, b):
    return func(a, b)
    
# 확인하면 잘 출력됨을 알 수 있다.
g(f, 1, 2)
```
```
3
```
#### 2. 함수를 variable로 전달할 수 있는가
```python
# 함수를 변수에 할당
f_var = f

f          # <function __main__.f(a, b)>
f_var      # <function __main__.f(a, b)>

print(f)
print(f_var)
```
```
<function f at 0x000002D0C15A74C8>
<function f at 0x000002D0C15A74C8>
```
#### 3. return(반환값)으로 함수를 사용할 수 있는가
```python
def calc(kind):
    if kind == 'add':
        def add(a, b):
            return a + b
        return add
    elif kind == 'subtract':
        def subtract(a, b):
            return a - b
        return subtract
        
adder = calc('add')
# 함수를 return 값으로 받는 것이 가능
```

### 왜 first-class function임을 강조할까?
- 재사용성
```python
def square(x):
    return x * x

def my_map(func, arg_list):
    result = []
    for i in arg_list:
        result.append(func(i)) # square 함수 호출, func == square
    return result
    
num_list = [1, 2, 3, 4, 5]

squares = my_map(square, num_list)

print(squares)
```
```
[1, 4, 9, 16, 25]
```
- closure
    - 다른 함수의 지역변수를 그 함수가 종료된 이후에도 기억할 수 있음
```python
def logger(msg):
    def log_message():
        print('Log: ', msg)
    return log_message
    
log_hi = logger('Hi')
print(log_hi) # log_message 오브젝트 출력
log_hi() # 'Log: Hi'가 출력

del logger # 글로벌 네임스페이스에서 logger 오브젝트를 지움

# logger 오브젝트가 지워진 것을 확인
try:
    print(logger)
except NameError:
    print('NameError: logger는 존재하지 않습니다.')
    
log_hi() # logger가 지워진 뒤에도 'Log: Hi'가 출력됩니다.
```
```
<function log_message at 0x000002D0C18DD438>
Log: Hi
NameError: logger는 존재하지 않습니다.
Log: Hi
```

- 실용적인 예시
```python
# 단순한 일반 함수
def simple_html_tag(tag, msg):
    print('<{0}>{1}<{0}>'.format(tag, msg)
    
simple_html_tag('h1', '심플 헤딩 타이틀')

print('-' * 30)

# 함수를 리턴하는 함수
def html_tag(tag):
    def wrap_text(msg):
        print('<{0}>{1}<{0}>'.format(tag, msg)
    return wrap_text
    
print_h1 = html_tag('h1')
print(print_h1)
print_h1('첫 번째 헤딩 타이틀')
print_h1('두 번째 헤딩 타이틀')

print_p = hyml_tag('p')
print_p('이것을 패러그래프입니다.')
```
```
<h1>심플 헤딩 타이틀<h1>
------------------------------
<function wrap_text at 0x1007dff50>
<h1>첫 번째 헤딩 타이틀<h1>
<h1>두 번째 헤딩 타이틀<h1>
<p>이것은 패러그래프 입니다.<p>
```

출처
- [SCHOOL OF WEB, 파이썬-퍼스트클래스 함수](http://schoolofweb.net/blog/posts/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%8D%BC%EC%8A%A4%ED%8A%B8%ED%81%B4%EB%9E%98%EC%8A%A4-%ED%95%A8%EC%88%98-first-class-function/)
- [jinmang2/cs_bootcamp_python](https://github.com/jinmang2/cs_bootcamp_python/blob/master/bootcamp_2%EC%A3%BC%EC%B0%A8%20%EC%A0%95%EB%A6%AC.ipynb)
