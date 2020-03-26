# `nn.Parameter`

```python
import torch
from collections import OrderedDict

class Parameter(torch.Tensor):
    """
    A kind of Tensor that is to be considered a module parameter.
    """
    def __new__(cls, data=None, requires_grad=True):
        if data is None:
            data = torch.Tensor()
        return torch.Tensor._make_subclass(cls, data, requires_grad)
    
    def __deepcopy__(self, memo):
        if id(self) in memo:
            return memo[id(self)]
        else:
            result = type(self)(self.data.clone(memory_format=torch.preserve_format),
                                self.requires_grad)
            memo[id(self)] = result
            return result
    
    def __repr__(self):
        return 'Parameter containing:\n' + super(Parameter, self).__repr__()
    
    def __reduce_ex__(self, proto):
        """
        < 자신의 객체 피클링하기 >
        
        `__reduce__(self)`: 확장 타입(즉, 파이썬의 C API를 사용하여 구현된 타입)을
            정의할 때 파이썬에서 피클링하려는 경우 피클링 방법을 지정.
            `__reduce__()`는 정의된 객체가 피클될 때 호출.
            파이썬이 찾고 피클하는 전역 이름을 나타내는 문자열 또는 튜플을 반환할 수 있음.
            튜플은 2~5개 요소를 포함
                (
                    객체를 다시 생성하기 위해 호출되는 호출 가능 객체,
                    호출 가능 객체에 대한 인수의 튜플,
                    `__setstate__`에 전달될 상태 (선택 사항),
                    피클링될 리스트 항목을 생성하는 반복자 (선택 사항),
                    피클링할 딕셔너리 항목을 생성하는 반복자 (선택 사항)
                )
                
        `__reduce_ex__(self)`: 호환성을 위해 존재.
        """
        # See Note [Don't serialize hooks]
        return (
            torch.utils._rebuild_parameter,
            (self.data, self.requires_grad, OrderedDict())
        )
```
