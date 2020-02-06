# Override Method
텐서플로 Estimator를 공부하다가 다른 코드 사용법을 알게되었따...☆

```python
class Estimator(object):
    def __init__(self, ...):
        ...
        self.__class__._assert_members_are_not_overridden(self)
       ... 
    ...
    def _assert_members_are_not_overridden(self):
        # Asserts members of `Estimator` are not overridden.
        _assert_members_are_not_overridden(Estimator, self)
    ...

def _assert_members_are_not_overridden(cls, obj):
    """Assert Estimator methods are not overwritten."""
    # TPUEstimator is special cased (owned by TF).
    if obj.__class__.__name__ == 'TPUEstimator':
        return
```
- 좀 더 공부해야하지만
- 우선 아래 함수처럼 써서 언제든 변화시킬 수 있는지..? 확인을 해봐야겠다...?
