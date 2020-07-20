```python
from dataclasses import dataclass, field
from functools import partial
import uuid


@dataclass
class item:
    id: int; name: str
    

@dataclass
class Factory:
    id: 'typing.Any'= field(default_factory=partial(uuid.uuid4))
    items: 'typing.Any'= field(default_factory=list)


f1 = Factory()
print(f1.items)
f1.items += ['apple', 'banana']
print(f1.items)
print(f1)
```

```
[]
['apple', 'banana']
Factory(id=UUID('6638fdea-40a3-4134-a74b-c396b846a56c'), items=['apple', 'banana'])
```

## 참고
- https://sjquant.tistory.com/30
- https://stackoverflow.com/questions/49931096/how-to-add-a-dataclass-field-without-annotating-the-type
