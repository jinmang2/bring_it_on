# array에서 bytes로, bytes에서 array로

### 블로그 설명
출처: https://d-tail.tistory.com/32
```python
import numpy as np
np.random.seed(42)

a = np.random.random(size=(3, 2, 2))
a
>>> array([[[0.37454012, 0.95071431],
>>>         [0.73199394, 0.59865848]],
>>> 
>>>        [[0.15601864, 0.15599452],
>>>         [0.05808361, 0.86617615]],
>>> 
>>>        [[0.60111501, 0.70807258],
>>>         [0.02058449, 0.96990985]]])

a.tobytes()
>>> b'\xecQ_\x1ew\xf8\xd7?T\xd6\xbbh@l\xee?Qg\x1e\x8f~l\xe7?\xb0,c\xd65(\xe3?\x84!"7k\xf8\
    xc3?L\x7f\x99\xe1\xa0\xf7\xc3?pUd\x9d"\xbd\xad?\xb5\xb7U\t\xb7\xb7\xeb?\xadK\x92\x8cU<\
    xe3?\x82\x82\x9a\xd2\x87\xa8\xe6?\x80~8\x07\x1a\x14\x95?\xa5S\xe3b\x80\t\xef?'

b = a.tobytes()
np.frombuffer(b, dtype=np.float64)
>>> array([0.37454012, 0.95071431, 0.73199394, 0.59865848, 0.15601864,
>>>        0.15599452, 0.05808361, 0.86617615, 0.60111501, 0.70807258,
>>>        0.02058449, 0.96990985])

np.frombuffer(b, dtype=np.float64).reshape(*a.shape)
>>> array([[[0.37454012, 0.95071431],
>>>         [0.73199394, 0.59865848]],
>>> 
>>>        [[0.15601864, 0.15599452],
>>>         [0.05808361, 0.86617615]],
>>> 
>>>        [[0.60111501, 0.70807258],
>>>         [0.02058449, 0.96990985]]])
```

### Python의 `array.array` 모듈 이해하기
출처: https://www.slideshare.net/dahlmoon/20160122-2

- array 클래스를 이용해 동일한 타입값(typecode)으로 인스턴스를 생성하기
```python
array.array(typecode[, initializer])
```
- array.array 지정 시 타입코드
```python
import array
print(array.typecodes)
>>>bBuhHiIlLqQfd
```

| type code | C Type             | Python Type       | Minimum size in bytes |
|:---------:|:------------------:|:-----------------:|:---------------------:|
| 'b'       | signed char        | int               | 1                     |
| 'B'       | unsigned char      | int               | 1                     |
| 'u'       | Py_UNICODE         | Unicode character | 2                     |
| 'h'       | signed short       | int               | 2                     |
| 'H'       | unsigned short     | int               | 2                     |
| 'i'       | signed int         | int               | 2                     |
| 'I'       | unsigned int       | int               | 2                     |
| 'l'       | signed long        | int               | 4                     |
| 'L'       | unsigned long      | int               | 4                     |
| 'q'       | signed long long   | int               | 8                     |
| 'Q'       | unsigned long long | int               | 8                     |
| 'f'       | float              | float             | 4                     |
| 'd'       | double             | float             | 8                     |
