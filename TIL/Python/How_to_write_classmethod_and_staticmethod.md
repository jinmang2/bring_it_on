link: https://julien.danjou.info/guide-python-static-class-abstract-methods/

```python
class Test:
    num = 0
    @staticmethod
    def add(x, y):
        return x + y
print(Test.add(1, 1)) # 클래스에서 직접 접근, 
                      # 객체별로 달라지는 것이 아니라 함께 공유
                      # 결과는 2

class Test:
    num = 0
    @staticmethod
    def add(x, y):
        return x + y

t = Test()
print(t.add(1, 1)) # 객체를 통해서 정적함수를 호출하는데 아무 이상 X
                   # 결과는 2
                   
# 파이썬은 막나간다.
class TestTestTestTest:
    num = 10
    @staticmethod
    def add(x, y):
        return x + y + self.num # TestTestTestTest이면 가능
    
t = TestTestTestTest()
print(t.add(1, 1)) # 정적함수이기 때문에 당연히 self를 통한 접근은 불가능

```
```
# 결과 화면
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-25-dcbf3388e91a> in <module>
      7 
      8 t = TestTestTestTest()
----> 9 print(t.add(1, 1)) # 정적함수이기 때문에 당연히 self를 통한 접근은 불가능

<ipython-input-25-dcbf3388e91a> in add(x, y)
      4     @staticmethod
      5     def add(x, y):
----> 6         return x + y + self.num # TestTestTestTest이면 가능
      7 
      8 t = TestTestTestTest()

NameError: name 'self' is not defined
---------------------------------------------------------------------------

```
```python
# classmethod
class Test:
    num = 10
    @classmethod
    def add(x, y):
        return x + y

print(Test.add(1, 1))
```
```
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-26-fea800e52b37> in <module>
      6         return x + y
      7 
----> 8 print(Test.add(1, 1))

TypeError: add() takes 2 positional arguments but 3 were given
---------------------------------------------------------------------------
```
```python
class Test:
    num = 10
    @classmethod
    def add(cls, x, y): # 쿨래스 인자 자체를 첫번째 인자로 넣어줘야 함
        return x + y

print(Test.add(1, 1))   # 결과는 2

# coding: utf-8
class Date:
    word = 'date : '
    def __init__(self, date):
        self.date = self.word + date
    @staticmethod
    def now():
        return Date('today')
    def show(self):
        print(self.date)

a = Date('2016, 9, 13')
a.show()
b = Date.now()
b.show()
>> date : 2016, 9, 13
>> date : today

class KoreanDate(Date):
    word = '날짜 : '
    
a = KoreanDate.now()
a.show()
>> date : today

# coding: utf-8
class Date :
    word = 'date : '
    def __init__(self, date):
        self.date = self.word + date
    @classmethod
    def now(cls):
        return cls("today")
    def show(self):
        print(self.date)

class KoreanDate(Date):
    word = '날짜 : '

a = KoreanDate.now()
a.show()
>> 날짜 : today
```
```
클래스라는 네임스페이스로 묶고 싶은 정적 메소드는 모두 @classmethod를 이용해서 사용하면 될 것 같지만
상속에서 사용되어 혼동을 초래할 여지가 없거나 조금이라도 더 간략하게 표현하고 싶을 경우 @staticmethod를 사용하는게 더 편해보임
```
