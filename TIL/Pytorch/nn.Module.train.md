# `nn.Module.train(self, mode=True)`
- `self.training`을 `mode`값으로 설정
- 하위 자식 모듈의 `self.training`도 `mode`값으로 설정
```python
...
def train(self, mode=True):
    self.training = mode
    for module in self.children():
        module.train(mode)
    return self
...
```

## 뿌리는 아래와 같다.
```python
def children(self):
    for name, module in self.named_children():
        yield module
```
```python
...
def named_children(self):
    memo = set() # memoization
    for name, module in self._modules.items():
        if module is not None and module not in memo:
            memo.add(module)
            yield name, module
...
```
```python
...
_version = 1
def __init__(self):
    torch._C._log_api_usage_once("python.nn_module")
    self.training = True
    ...
    self._modules = OrderedDict()
...
```

## `._modules`를 사용하는 `method`는 아래와 같다.
- `.add_module()`
- `.__getattr__(self, name)`
- `.__setattr__(self, name, value)`
- `.__delattr__(self, name)`
- `.state_dict(self, destination=None, prefix='', keep_vars=False)`
- `.load_from_state_dict(self, state_dict, prefix, local_metadata, strict, missing_keys, unexpected_keys, error_msgs)`
- `.named_modules(self, memo=None, prefix='')`
- `.__repr__(self)`
- `.__dir__(self)`
- `._replicate_for_data_parallel(self)`

## `eval`메서드는 mode를 False로 
