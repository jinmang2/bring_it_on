# Python Decorator

## Decorator?
- 기존의 코드에 여러가지 기능을 추가하는 파이썬 구문
- 안 어려우니 걱정 니니

## 뭐가 안어려워? 개어렵던데 -- 코드로 공부!

- case 1. closure? decorator?
```python
def outer_function(msg):
    def inner_function():
        print(msg)
    return inner_function
    
h1_func = outer_function('Hi')
bye_func = outer_function('Bye')

h1_func()
bye_func()
```
위는 closure. closure와 decorator는 함수를 다른 함수의 인자로 전달한다는 점이 다름! (다르달까, 데코레이터는 함수에 기능을 추가하는 것이기 때문에 인자로 함수를 넘겨주는 느낌?)

```python
def decorator_function(orig_function):              #1
    def wrapper_function():                         #5
        return orig_function()                      #7
    return wrapper_function                         #6
    
def display():                                      #2
    print('display 함수가 실행됐습니다.')             #8
    
decorator_display = decorator_function(display)     #3

decorator_display()                                 #4
```
```
display 함수가 실행됐습니다.
```
- case 2. decorator 왜 써요?
```python
# -*- coding: utf-8 -*-
def decorator_function(orig_function):
    def wrapper_function():
        print('{} 함수가 호출되기전 입니다.'.format(original_function.__name__))
        return orig_function()
    return wrapper_function

def display_1():
    print('display_1 함수가 실행됐습니다.')

def display_2():
    print('display_2 함수가 실행됐습니다.')

display_1 = decorator_function(display_1)
display_2 = decorator_function(display_2)

display_1()
print()
display_2()
```
```
display_1 함수가 호출되기전 입니다.
display_1 함수가 실행됐습니다.

display_2 함수가 호출되기전 입니다.
display_2 함수가 실행됐습니다.
```

- case 3. "@" 심볼과 데코레이터 함수의 이름을 붙여 간단한 구문으로 사용
case 2.의 코드를 간단하게 만들자.
```python
# -*- coding: utf-8 -*-
def decorator_function(orig_function):
    def wrapper_function():
        print('{} 함수가 호출되기전 입니다.'.format(original_function.__name__))
        return orig_function()
    return wrapper_function

@decorator_function
def display_1():
    print('display_1 함수가 실행됐습니다.')

@decorator_function
def display_2():
    print('display_2 함수가 실행됐습니다.')

# display_1 = decorator_function(display_1)
# display_2 = decorator_function(display_2)

display_1()
print()
display_2()
```
```
display_1 함수가 호출되기전 입니다.
display_1 함수가 실행됐습니다.

display_2 함수가 호출되기전 입니다.
display_2 함수가 실행됐습니다.
```

- case 4. input이 있는 함수에 기능 추가
```python
# -*- coding: utf-8 -*-
def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):  #1
        print('{} 함수가 호출되기전 입니다.'.format(original_function.__name__))
        return original_function(*args, **kwargs)  #2
    return wrapper_function


@decorator_function
def display():
    print('display 함수가 실행됐습니다.')


@decorator_function
def display_info(name, age):
    print('display_info({}, {}) 함수가 실행됐습니다.'.format(name, age))

display()
print()
display_info('John', 25)
```
```
display 함수가 호출되기전 입니다.
display 함수가 실행됐습니다.

display_info 함수가 호출되기전 입니다.
display_info(John, 25) 함수가 실행됐습니다.
```

- case 5. class 형식의 decorator (잘 사용하진 않음)
```python
class DecoratorClass:  #1
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, *args, **kwargs):
        print('{} 함수가 호출되기전 입니다.'.format(self.original_function.__name__))
        return self.original_function(*args, **kwargs)


@DecoratorClass  #2
def display():
    print('display 함수가 실행됐습니다.')


@DecoratorClass  #3
def display_info(name, age):
    print('display_info({}, {}) 함수가 실행됐습니다.'.format(name, age))

display()
print()
display_info('John', 25)
```
```
display 함수가 호출되기전 입니다.
display 함수가 실행됐습니다.

display_info 함수가 호출되기전 입니다.
display_info(John, 25) 함수가 실행됐습니다.
```

- case 6. 실제 프로젝트에서 데코레이터가 사용되는 예제 > logging
```
# -*- coding: utf-8 -*-
import datetime
import time


def my_logger(original_function):
    import logging
    logging.basicConfig(filename='{}.log'.format(original_function.__name__), level=logging.INFO)
    
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        logging.info(
            '[{}] 실행결과 args - {}, kwargs - {}'.format(timestamp, args, kwargs))
        return original_function(*args, **kwargs)

    return wrapper


def my_timer(original_function):  #1
    import time

    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = original_function(*args, **kwargs)
        t2 = time.time() - t1
        print('{} 함수가 실행된 총 시간: {} 초'.format(original_function.__name__, t2))
        return result

    return wrapper


@my_timer  #2
def display_info(name, age):
    time.sleep(1)
    print('display_info({}, {}) 함수가 실행됐습니다.'.format(name, age))

display_info('John', 25)
```

- case 7. 복수의 데코레이터 사용하기 using `functools.wraps`
```python
# -*- coding: utf-8 -*-
from functools import wraps
import datetime
import time


def my_logger(original_function):
    import logging
    logging.basicConfig(filename='{}.log'.format(original_function.__name__), level=logging.INFO)
    
    @wraps(original_function)  #1
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        logging.info(
            '[{}] 실행결과 args - {}, kwargs - {}'.format(timestamp, args, kwargs))
        return original_function(*args, **kwargs)

    return wrapper


def my_timer(original_function):
    import time

    @wraps(original_function)  #2
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = original_function(*args, **kwargs)
        t2 = time.time() - t1
        print '{} 함수가 실행된 총 시간: {} 초'.format(original_function.__name__, t2)
        return result

    return wrapper


@my_timer
@my_logger
def display_info(name, age):
    time.sleep(1)
    print 'display_info({}, {}) 함수가 실행됐습니다.'.format(name, age)

display_info('Jimmy', 30)  #3
```

출처
- [SCHOOL OF WEB, 파이썬 - 데코레이터](http://schoolofweb.net/blog/posts/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%8D%B0%EC%BD%94%EB%A0%88%EC%9D%B4%ED%84%B0-decorator/)
- [tistory, python decorator 어렵지 않아요](https://bluese05.tistory.com/30)
