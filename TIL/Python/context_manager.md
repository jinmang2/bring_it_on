# Context Manager

- Use `class`
```python
# context_manager1.py
class File:
    def __init__(self, filename, method):
        self.file = open(filename, method)

    def __enter__(self):
        print('Enter')
        return self.file

    def __exit__(self, type, value, traceback):
        print(f'{type}, {value}, {traceback}')
        print('Exit')
        self.file.close()
        if type == Exception:
            return True

with File("file.txt", "w") as f:
    print('Middle')
    f.write('hello!')
    raise Exception('I Love you, ')
    raise ValueError('Me too!')
```
```
Enter
Middle
<class 'Exception'>, I Love you, , <traceback object at 0x000001715F573CC8>
Exit
[Finished in 0.064s]
```

- Use `decorator`
```python
from contextlib import contextmanager

@contextmanager
def file(filename, method):
    file = open(filename, method)
    yield file
    file.close()

with file('text.txt', 'w') as f:
    print('middle')
    f.write('hello!')
```
```
middle
[Finished in 0.07s]
```

출처: https://www.youtube.com/watch?v=Lv1treHIckI
