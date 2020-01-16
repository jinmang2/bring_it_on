# Overloading vs Overriding
- 객체 지향 개념
- 객체를 지정하고 한번만 사용하고 약간 내용이 바뀐 것을 다시 객체로 만들어서 해야 한다면 상당히 비효율적
- 재사용 관점으로 이해
  - 오버로딩
    - 함수를 호출할 때 동일한 이름의 함수로 정의하되 인자의 값을 형태나 개수로 달리하는 것
    - 호출할 때 인자의 값이나 개수를 넣으면 알아서 해당 함수로 불리는 것
  - 오버라이딩
    - 객체지향에서 상속에는 부모와 자식이 존재
    - 부모에서는 개념만 정의하고 결국 자식이 그 뜻을 이루기도 함
    - 부모에서 선언만 하고, 자식이 그 내용을 채우는 경우가 오버라이딩
    - 동일한 함수여야하며 동일한 인자여야 한다.
    
## 코드로?
- 함수 오버로딩: Overloading
  - 함수이름이 같고 매개 변수의 타입과 갯수가 다른 함수들을 의미
```python
def foo(a):...

def foo(a, b):...
```
- 함수 오버라이딩: Overriding
  - 부모 클래스의 정의한 메서드를 자식 클래스에서 변경하는 것
- 연산자 오버로딩: Overloading
  - 객체의 연산자를 새로 정의해서 사용하는 것!
```python
class Order:
    def __init__(self, amount):
        self.amount = amount
        
    def __add__(self, other):
        return Order(self.amount + other.amount)
        
o1 = Order(100)
o2 = Order(300)
print(o1.amount)
o1 += o2
print(o1.amount)
```
