```python
from functools import reduce


users = [
    {'mail': 'gregorythomas@gmail.com', 'name': 'Brett Holland', 'sex': 'M', 'age': 73},
    {'mail': 'hintoncynthia@hotmail.com', 'name': 'Madison Martinez', 'sex': 'F', 'age': 29},
    {'mail': 'wwagner@gmail.com', 'name': 'Michael Jenkins', 'sex': 'M', 'age': 51},
    {'mail': 'daniel79@gmail.com', 'name': 'Karen Rodriguez', 'sex': 'F', 'age': 32},
    {'mail': 'ujackson@gmail.com', 'name': 'Amber Rhodes', 'sex': 'F', 'age': 42}
]

# reduce(집계 함수, 순회 가능한 데이터[, 초기값])
reduce(lambda acc, cur: acc + cur["age"], users, 0)
```

# 출처: https://www.daleseo.com/python-functools-reduce/
