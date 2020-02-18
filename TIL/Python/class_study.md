# Python Class 탐구생활 :)

출처: https://ziwon.dev/post/python_magic_methods/

```python
class CuteDecorator:
    def __init__(self, data):
        self.storage = data
    def __call__(self):
        print('data entered :',self.storage.__name__)
        self.storage()
        print('data exited :',self.storage.__name__)

@CuteDecorator
def printer():
    print('I print the empty space')
    pass

print('---start---')
printer()
```
```
---start---
data entered : printer
I print the empty space
data exited : printer
```
```python
class A:
    def __init__(self):
        print('init')
    def __call__(self):
        print('call')
    def __repr__(self):
        return 'a에용 뿌잉뿌잉'
    def __str__(self):
        return '사랑해'
        
a = A()
>>> init
a()
>>> call
a
>>> a에용 뿌잉뿌잉
str(a)
>>> '사랑해'
print(a)
>>> 사랑해
repr(a)
'a에용 뿌잉뿌잉'
```
