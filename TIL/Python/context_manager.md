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

---

# Context Manager 내용 추가

- 파이썬의 `with`문은 코드를 특별한 컨텍스트에서 실행함을 나타내는 데 사용
- 예로, with문에 상호 배제 잠금을 사용하여 잠금이 설정되어 있는 동안만 들여 쓴 코드를 실행함을 나타냄
    ```python
    from threading import Lock
    lock = Lock()
    with lock:
        print('Lock is held')
    ```
- Lock 클래스가 with 문을 제대로 지원하는 덕분에 위의 코드는 아래 try/finally 구문에 상응
    ```python
    lock.acquire()
    try:
        print('Lock is held')
    finally:
        lock.release()
    ```
- 내장 모듈 `contextlib`을 사용하면 객체와 함수를 with문에 사용할 수 있게 만들기가 쉬움
- 이 데코레이터를 이용하는 방법이 위의 `__enter__`와 `__exit__`라는 특별한 메서드를 담은 새 클래스를 정의하는 방법(표준방법)보다 훨씬 쉬움
- 아래 예시를 보자
    ```python
    import logging
    
    def my_function():
        logging.debug('Some degug data')
        logging.error('Error log hear')
        logging.debug('More debug data')
        
    # 이 프로그램의 기본 로그 수준은 WARNING. 따라서 함수를 실행하면 오류메세지만 출력
    my_function()
    # 결과
    # ERROR:roor:Error log hear
    ```
- 컨텍스트 매니저를 정의하여 이 함수의 로그 수준을 임시로 높이는 것이 가능
- 아래 내용은 블로그 참고

- 막 둘 블로그,
- 아래 코드를 보자
    ```python
    from contextlib import contextmanager
    
    @contextmanager
    def open_file(name):
        f = open(name, 'wb')
        yield f
        f.close()
- 위는 아래의 기능을 처리
    1. 파이썬이 `yield` 키워드를 만난다면, 일반적인 함수 대신에 제너레이터를 만들었기 때문
    2. 데코레이션이 있기 때문에 컨텍스트 매니저는 함수 이름(open_file)을 전달 인자로 호출
    3. `contextmanager` 함수는 `GeneratorContextManager`로 감싸진 제너레이터를 반환
    4. `GeneratorContextManager`는 `open_file` 함수를 할당. 그렇기 때문에 `open_file` 함수를 앞으로 호출하면, 사실은 `GeneratorContextManager`를 호출하는 것.
    ```python
    with open_file('some_file') as f:
        f.write('Hola)
    ```

출처:
- https://brownbears.tistory.com/240
- https://docs.python.org/3/library/contextlib.html
- https://sjquant.tistory.com/12
- https://python.flowdas.com/library/contextlib.html
- https://ddanggle.gitbooks.io/interpy-kr/ch24-context-manager.html
- https://soooprmx.com/archives/4079
