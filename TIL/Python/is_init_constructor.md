# 과연 `__init__`이 생성자인가?
- 생성자로 객체생성을 호출받으면 먼저 `__new__`를 호출하여 객체를 생성할당하고,
- `__new__`메서드가 `__init__`메서드를 호출하여 객체에서 사용할 초기값들을 초기화함
- 일반적으로 파이썬에서 클래스를 만들 시 `__init__` 메서드만 오버라이딩하여 객체초기화에 이용
```python
class Flight:

    def __init__(self):
        print('init')
        super().__init__()
        
    def __new__(cls):
        print('new')
        return super().__new__(cls)
        
    def number(self):
        return 'SN060'

f = Flight()
>>> new
>>> init
```

출처: https://suwoni-codelab.com/python%20%EA%B8%B0%EB%B3%B8/2018/03/08/Python-Basic-class/
