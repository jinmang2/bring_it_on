## Link
- https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d

## 어떤 역할?
- 함수의 작동 시간을 측정하고 이를 마이크로초/초/분/시 단위로 출력한다.

## 코드는?
```python
import time
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('\'{:s}\'  {:2.2f} ms  {:2.2f} sec  {:2.2f} min  {:2.2f} hour'.format(
                  method.__name__, (te - ts) * 1000, (te - ts), (te - ts) / 60, (te - ts) / 3600))
        return result
    return timed

# 아래와 같은 방식으로 사용한다.
@timeit
def test():
    res = []
    for i in range(100000):
        res.append(i)
        
test()
```
```
'test'  12.96 ms  0.01 sec  0.00 min  0.00 hour
```
