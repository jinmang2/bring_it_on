# \_\_str\_\_, \_\_repr\_\_ 이해
```python
def add_expr(a, b):
    return str(a) + ' + ' + str(b)

add_expr(3, 5)
```
```
'3 + 5'
```
**`str`은 입력받은 객체의 문자열 버전을 반환하는 함수.**<br>
**`str`은 내장 함수가 아니고 파이썬의 기본 내장 클래스**<br>
즉, `str(3)`처럼 입력하는 것은 내장 함수 `str`이 실행되는 것이 아니고 사실 **내장 `str`클래스의 생성자 메소드를 실행, 그 인자를 3으로 주는 것과 같다.**
<br>
## str vs \_\_str\_\_
파이썬에는 내장된 많은 자료형들에, 해당하는 자료형에 대한 연산을 정의하는 메소드들이 있음<br>
그 메소드들은 메소드의 이름 앞뒤에 '__'(double underscore)를 지님<br>
- 3 + 5가 어떻게 실행될까?
```python
# 1.
>>> 3 + 5 # 내부적으로 및 문장을 실행!
>>> (3).__add__(5) # (3)처럼 ()로 감싸야 한다. 소수와 구별해야 하기 때문.

8

# 2.
>>> [1, 2, 3] + [4, 5, 6] # 내부적으로 밑 문장을 실행!
>>> [1, 2, 3].__add__([4, 5, 6])

[1, 2, 3, 4, 5, 6]
```
첫 번째 예시는 정수 3에 정수 5를 더해 결과 8을 출력<br>
두 번째 예시는 `+`연산자에 대해 클래스마다 다른 구현이 되어 있음을 보여줌<br>
list 자료형은 `+` 연산에 대해 값을 더하는 것이 아닌 접합(concatenate)을 하고 새로 생성된 list를 반환<br>
**실제로 클래스들에서 구현하는 위와 같은 메소드들을 `Magic method`라고 하며 매우 많은 목록이 존재한다.)**<br>

어떤 객체 object에 `str`, `repr` 함수를 씌우면 해당 객체의 클래스에 정의되어 있는 `__str__`, `__repr__` 메서드가 해당 객체에서 실행되고, 두 메소드에 있는 코드를 실행한다.<br>

## repr, \_\_repr\_\_
repr: Representation<br>
**표현은 어떤 객체의 '본질'보다는 외부에 노출되는, 사용자가 이해할 수 있는 객체의 모습을 표현**<br>

`repr`함수는 어떤 객체의 '출력될 수 있는 표현'(printable representation)을 문자열의 형태로 반환.
```python
import math

>>> repr(3)
>>> repr([1, 2, 3])
>>> repr(math)
```
```
'3'
'[1, 2, 3]'
"<module 'math' from ...>"
```

# \_\_str\_\_, \_\_repr\_\_ 공통점
두 메소드는 객체의 문자열 표현을 반환
    - 두 메소드는 객체가 어떤 데이터 타입이든지간에 객체의 문자열 표현을 반환
    - 왜 문자열 표현인가?
    - 일반적인 문자열 평문(plain text)은 파이썬을 사용하는 모든 인간들이 이해할 수 있는 Universal Interface이기 때문이다.
    - 유닉스의 철학 교리 중 프로그램이나 설정파일을 평문으로 작성하라는 설명은 이를 대변
    - 프로그램을 사용하는 것은 인간이고 인간에게 유익해야 한다.

# \_\_str\_\_, \_\_repr\_\_ 차이점
이 둘의 차이는 본질적으로 의도된 사용처가 다르다는 것에서 기인.
- `__str__`는 태생적인 목적 자체가 인자를 '문자열화'해 반환하라는 것
- 평문 문자는 Universal Interface이기 때문에, 서로 다른 데이터 타입이 상호작용하는 좋은 인터페이스가 된다.
```python
>>> a = 1
>>> b = '가'
>>> c = [1, 2, 3, 4, 5]
>>> print(a, b, c)
```
```
1 가 [1, 2, 3, 4, 5]
```
위가 가능한 이유는 **a, b, c에 해당하는 int, str, list 자료형이 각 객체를 '문자열'로 반환하는 `__str__` 메소드를 내부적으로 구현하고 있고, 문자열을 Universal Interface이기 때문에 출처가 서로 완전히 다른 자료형임에도 문자열화된 인자들을 매끄럽게 이을 수 있었기 때문**
<br>따라서 `__str__`의 본질적인 목적은 객체를 '표현'하는 것에 있다기보다는 추가적인 가공이나 다른 데이터와 호환될 수 있도록 문자열화하는 데 있다.

```python
class A:
    def __str__(self):
        return 'str method is called'

    def __repr__(self):
        return 'repr method is called'

>>> a = A()
 
>>> str(a)  # 1.
>>> a  # 2.

# Look at here!
>>> print(a)  # 3.

'str method is called' # 1.
repr method is called  # 2.

# Look at here!
str method is called   # 3.
```
- `__repr__`은 본 목적이 객체를 인간이 이해할 수 있는 평문으로 '표현'하라는 것

`__str__`가 서로 다른 자료형 간에 인터페이스를 제공하기 위해서 존재한다면, `__repr__`은 해당 객체를 인간이 이해할 수 있는 표현으로 나타내기 위한 용도.

## \_\_str\_\_, \_\_repr\_\_가 다른 예 만들어보기
```python
class A:
    # __str__ 은 구현하지 않는다.(다시 말해 overriding하지 않는다.)
    
    def __repr__(self):
        return str(id(self))

>>> a = A()
>>> a

140249540632704

###

# 1. A와 int를 다중상속하는 NewInt를 만든다.
class NewInt(A, int):
    pass


# 2. 인스턴스 생성
>>> n = NewInt(5)

# 3. __add__ 메소드 호출
>>> n + 5

10

# 4. __str__ 메소드 호출
>>> str(n)

'5'

# 5. __repr__ 메소드 호출
>>> repr(n)

'140249540506184'
```
객체의 표현을 값이 아닌 고유한 주소값으로 나타내는 클래스 A를 구현했다. 이 클래스는 `__repr__`만을 구현하고 있는데 그 결과 인스턴스를 표현할 때 고유한 메모리 주소값이 출력되게 됬다.



출처: https://shoark7.github.io/programming/python/difference-between-__repr__-vs-__str__

sub 출처:
- https://docs.python.org/3/library/functions.html#repr
- https://shoark7.github.io/programming/knowledge/what-is-rest.html
- https://shoark7.github.io/programming/knowledge/unix-philosophy-intro.html
- https://www.python-course.eu/python3_magic_methods.php
