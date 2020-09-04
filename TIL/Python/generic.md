# Generic
- 컨테이너에 보관된 객체에 대한 형 정보는 일반적인 방식으로 정적으로 유추될 수 없음.

```python
from typing import Mapping, Sequence

def notify_by_email(
    employees: Sequence[Employee],
    overrides: Mapping[str, str]
) -> None:
    ...
```

- 제네릭은 `TypeVar`라는 `typing`에서 제공하는 새로운 팩토리를 사용하여 매개 변수화될 수 있음
```python
from typing import Sequence, TypeVar

T = TypeVar('T') # 형 변수를 선언

def first(l: Sequence[T]) -> T: # 제네릭 함수
    return l[0]
```
