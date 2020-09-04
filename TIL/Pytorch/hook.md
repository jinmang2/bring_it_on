# Pytorch hook

```python
import torch 
import torch.nn as nn

class myNet(nn.Module):
  def __init__(self):
    super().__init__()
    self.conv = nn.Conv2d(3,10,2, stride = 2)
    self.relu = nn.ReLU()
    self.flatten = lambda x: x.view(-1)
    self.fc1 = nn.Linear(160,5)
   
  
  def forward(self, x):
    x = self.relu(self.conv(x))
    return self.fc1(self.flatten(x))
  

net = myNet()

def hook_fn(m, i, o):
  print(m)
  print("------------Input Grad------------")
  for grad in i:
    try:
      print(grad.shape)
    except AttributeError: 
      print ("None found for Gradient")
  print("------------Output Grad------------")
  for grad in o:  
    try:
      print(grad.shape)
    except AttributeError: 
      print ("None found for Gradient")
  print("\n")
  
net.conv.register_backward_hook(hook_fn)
net.fc1.register_backward_hook(hook_fn)
inp = torch.randn(1,3,8,8)
out = net(inp)

(1 - out.mean()).backward()
```

### 출처: https://blog.paperspace.com/pytorch-hooks-gradient-clipping-debugging/


# 다시 정리
# torch hook 정리
```
@도요새 님 답변이 굉장히 늦었는데,

torch 1.6.0 기준으로,
register_forward_hooks는 hook_fn함수를 모듈에 등록시키는 함수,
_forward_pre_hooks, _backward_hooks, _forward_hooks는 
등록한 hook_fn을 저장할 OrderedDict객체입니닷!!

hook_fn은 torch에서 layer연산을 forward메서드로 정의하면 
__call__ 메서드에서 forward함수를 호출해서 layer연산을 진행하는데, 
여기서 hook_fn을 ``등록``하여 기울기값을 디버깅하거나 반환받도록하는 역할 수행합니당

저도 다시 찾아보면서 코드 확인해봤는데,
도요새님 워낙 뛰어나시니 코드보시면 이해 더 빠르실 것 같아요
```
```python
class Module:

    dump_patches: bool = False

    _version: int = 1

    training: bool

    def __init__(self):
        """
        Initializes internal Module state, shared by both nn.Module and ScriptModule.
        """
        torch._C._log_api_usage_once("python.nn_module")

        self.training = True
        self._parameters = OrderedDict()
        self._buffers = OrderedDict()
        self._non_persistent_buffers_set = set()
        self._backward_hooks = OrderedDict()
        self._forward_hooks = OrderedDict()
        self._forward_pre_hooks = OrderedDict()
        self._state_dict_hooks = OrderedDict()
        self._load_state_dict_pre_hooks = OrderedDict()
        self._modules = OrderedDict()
    
    ...
    def _call_impl(self, *input, **kwargs):
        for hook in itertools.chain(
                _global_forward_pre_hooks.values(),
                self._forward_pre_hooks.values()):
            result = hook(self, input)
            if result is not None:
                if not isinstance(result, tuple):
                    result = (result,)
                input = result
        if torch._C._get_tracing_state():
            result = self._slow_forward(*input, **kwargs)
        else:
            result = self.forward(*input, **kwargs)
        for hook in itertools.chain(
                _global_forward_hooks.values(),
                self._forward_hooks.values()):
            hook_result = hook(self, input, result)
            if hook_result is not None:
                result = hook_result
        if (len(self._backward_hooks) > 0) or (len(_global_backward_hooks) > 0):
            var = result
            while not isinstance(var, torch.Tensor):
                if isinstance(var, dict):
                    var = next((v for v in var.values() if isinstance(v, torch.Tensor)))
                else:
                    var = var[0]
            grad_fn = var.grad_fn
            if grad_fn is not None:
                for hook in itertools.chain(
                        _global_backward_hooks.values(),
                        self._backward_hooks.values()):
                    wrapper = functools.partial(hook, self)
                    functools.update_wrapper(wrapper, hook)
                    grad_fn.register_hook(wrapper)
        return result

    __call__ : Callable[..., Any] = _call_impl
    
```
```python
def register_hook(
    self,
    hook: Callable[['Module', _grad_t, _grad_t], Union[None, Tensor]]
) -> RemovableHandle:
    """
    psuedo code for Module's register hook_fn
    _hooks는 아래 세 가지 중 하나
        ``_forward_pre_hooks``
        ``_forward_hooks``
        ``_backward_hooks``
    attr: ``hook``은 아래와 같은 함수
        # 아래 함수를 정의하여 gradient를 쉽게 다룰 수 있음
        # 코드가 돌아가며 gradient가 어떻게 변화하는지 디버깅하거나
        # 중간에 결과값을 반환하여 다른 작업 등을 할 수 있음
        def hook_fn(module, grad_input, grad_output):
            print(grad_input)
            print(grad_output)
            return (grad_input, grad_output)
    hook 등록 메서드가 작동하는 방식은 단순히 추가하는 방식
    """
    handle = RemovableHandle(self._hooks)
    self.hooks[handle.id] = hook
    return handle
```
