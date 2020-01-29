# 이미 정의된 `class`에 함수를 부여하기
- 이는 챗봇을 구현하려고 dialog창 객체 구상을 하다가 시작된 의문점이었다.
- 아래의 역할을 하는 것을 구현할 수 있을까?
    - `class`를 우선 정의
    - 그 후에 메서드를 추가. (코드로 쓰지않고)
- 이를 어떻게 검색할지 감도 안잡혀서;; 어떻게 해결할까 고민하다가
- 아래 두 가지 방식으로 해결했다.

### 1. `method overriding`
- 부모의 메서드를 다시 쓰는 것.
- 마치 청출어람이랄까
```python
class Test:
    def __init__(self):
        self.__height = 5
        self.__width = 17
        
    @property
    def height(self):
        return self.__height
        
    @property
    def width(self):
        return self.__width
        
    @height.setter
    def height(self, h):
        self.__height = h
        
    @width.setter
    def width(self, w):
        self.__width = w
```
- 위와 같은 객체가 있다고 가정하자.
- 아래와 같이 위의 객체를 상속받아 메서드 오버라이딩을 실시하여 내가 원하는 바를 이룰 수 있다.
    - 상속 자체가 코드 사용성 늘리고 메서드를 재정의할 수 있는 장점이 있으니께!
    - 그러나 객체를 새로 만드는 것과 동일하고 같은 조건을 가지는 함수도 새로 만들 dialog 숫자만큼 만들어야 하는 단점이 존재한다.
```python
class Test2(Test):
    def __init__(self):
        super().__init__()
        
    def new_cond(self):
        return self.height * self.width
        
t2 = Test2()
t2.new_cond()
>>> 85
```
- 그래서 이게 될까? 싶었는데 되서 깜짝 놀란 방법이 아래 방법이다.

### 2. 함수를 새로 정의하기
```python
 def new_cond(self):
    return self.height + self.width
    
t = Test()
new_cond(t) # 딱 내가 원하는 모양!!! 이거면 조건절을 정의해놓고 코드 재사용을 할 수 있다!!
            # 심지어 상속처럼 객체를 만들 때마다 복붙이 아닌 메서드를 추가하는 것처럼 사용 가능!
>>> 85
t.new_cond = new_cond
t.new_cond()
```
```
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-48-7d189074a6c4> in <module>
----> 1 t.new_cond()

TypeError: new_cond() missing 1 required positional argument: 'self'
 ```
 
 
