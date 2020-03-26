# `Optimizer().zero_grad()`
- Clears the gradients of all optimized

```python
# torch.optim.optimizer.py
...
class Optimizer(object):
    def __init__(self, params, defaults):
        torch._C._log_api_usage_once("python.optimizer")
        self.defaults = defaults
        ...
        self.param_groups = []
        
        params_groups = list(params)
        if len(param_groups) == 0:
            raise ValueError("optimizer got an empty parameter list")
        if not isinstance(param_groups[0], dict):
            param_groups = [{'params': param_groups}]
        ...
    ...
    def zero_grad(self):
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is not None:
                    p.grad.detach_()
                    p.grad.zero_()
    ...
...
```

- 직접 예시를 보자.
- RNN Encoder-Decoder에서 사용한 Seq2Seq 모델로 확인을 할 것임
```python
...
model = Seq2Seq(enc, dec, device).to(device)

def init_weights(m):
    for name, param in m.named_parameters():
        nn.init.normal_(param.data, mean=0, std=0.01)

print(len(list(model.parameters())))

model.apply(init_weights)
```
```
12

Seq2Seq(
  (encoder): Encoder(
    (embedding): Embedding(7855, 256)
    (rnn): GRU(256, 512)
    (dropout): Dropout(p=0.5, inplace=False)
  )
  (decoder): Decoder(
    (embedding): Embedding(5893, 256)
    (rnn): GRU(768, 512)
    (fc_out): Linear(in_features=1280, out_features=5893, bias=True)
    (dropout): Dropout(p=0.5, inplace=False)
  )
)
```
```python
import torch.optim as optim

# `Adam`은 `Optimizer` 클래스를 상속받음.
optimizer = optim.Adam(model.parameters())

print(optimizer.defaults)

print(optimizer.param_groups)
```
```
{'lr': 0.001,
 'betas': (0.9, 0.999),
 'eps': 1e-08,
 'weight_decay': 0,
 'amsgrad': False}
 
 [{'params': [Parameter containing:
tensor([[ 0.0017,  0.0032, -0.0024,  ...,  0.0002, -0.0033, -0.0140],
        [ 0.0047,  0.0047, -0.0030,  ...,  0.0081,  0.0210, -0.0032],
        [ 0.0019,  0.0046,  0.0114,  ..., -0.0086,  0.0045, -0.0026],
        ...,
        [-0.0018,  0.0028, -0.0112,  ..., -0.0019, -0.0049,  0.0060],
        [ 0.0121, -0.0077, -0.0036,  ..., -0.0029,  0.0076,  0.0045],
        [-0.0101,  0.0120, -0.0036,  ..., -0.0016, -0.0022,  0.0117]],
       device='cuda:0', requires_grad=True), Parameter containing:
tensor([[ 0.0210, -0.0161,  0.0171,  ...,  0.0029, -0.0135,  0.0092],
        [-0.0048, -0.0031, -0.0049,  ..., -0.0003, -0.0113, -0.0152],
        [ 0.0200, -0.0157, -0.0118,  ..., -0.0007, -0.0144,  0.0071],
        ...,
        [ 0.0033,  0.0110,  0.0104,  ..., -0.0049, -0.0070, -0.0061],
        [ 0.0051,  0.0036,  0.0121,  ...,  0.0084, -0.0057,  0.0067],
        [ 0.0085,  0.0004,  0.0154,  ..., -0.0051,  0.0028, -0.0059]],
       device='cuda:0', requires_grad=True), Parameter containing:
tensor([[ 1.1422e-02,  1.0581e-02,  8.0982e-03,  ...,  3.4510e-04,
          6.7090e-04,  1.1011e-02],
        [-9.5206e-03,  8.2878e-03,  4.7328e-05,  ...,  1.7655e-02,
         -3.6808e-03, -2.3644e-04],
        [-1.0137e-03, -8.4144e-03,  1.4422e-02,  ..., -4.0370e-03,
          7.9386e-03,  1.3761e-02],
        ...,
        [-1.4453e-03, -9.8543e-03, -8.9673e-03,  ...,  7.7568e-03,
          1.3797e-02, -4.5974e-03],
        [ 6.0108e-03,  1.4967e-02,  3.3005e-03,  ..., -1.6548e-02,
          3.7679e-03, -6.4066e-03],
        [-1.7056e-03,  1.7189e-03,  9.5006e-04,  ...,  3.8580e-03,
          2.0355e-02, -2.2992e-02]], device='cuda:0', requires_grad=True), Parameter containing:
tensor([-0.0127, -0.0140, -0.0045,  ...,  0.0120, -0.0122,  0.0113],
       device='cuda:0', requires_grad=True), Parameter containing:
tensor([-6.5787e-04,  3.7851e-03,  9.8841e-03,  ...,  2.9698e-03,
        -1.6876e-02,  8.4674e-05], device='cuda:0', requires_grad=True), Parameter containing:
tensor([[-0.0153, -0.0001,  0.0159,  ...,  0.0063, -0.0082, -0.0187],
        [ 0.0042,  0.0113, -0.0104,  ...,  0.0078, -0.0113,  0.0172],
        [ 0.0089,  0.0017,  0.0042,  ..., -0.0031,  0.0047, -0.0056],
        ...,
        [ 0.0020, -0.0018, -0.0044,  ..., -0.0076, -0.0170,  0.0144],
        [ 0.0049,  0.0047,  0.0136,  ..., -0.0050, -0.0134, -0.0012],
        [ 0.0125,  0.0047,  0.0126,  ..., -0.0035,  0.0032,  0.0186]],
       device='cuda:0', requires_grad=True), Parameter containing:
tensor([[-0.0013, -0.0098, -0.0015,  ...,  0.0135,  0.0089,  0.0113],
        [-0.0088, -0.0085,  0.0088,  ..., -0.0053, -0.0093, -0.0025],
        [ 0.0043, -0.0167, -0.0227,  ..., -0.0008,  0.0061,  0.0040],
        ...,
        [ 0.0020,  0.0052, -0.0091,  ..., -0.0221, -0.0088, -0.0114],
        [-0.0047, -0.0262, -0.0075,  ...,  0.0133,  0.0017,  0.0015],
        [ 0.0007, -0.0080, -0.0153,  ...,  0.0028, -0.0121,  0.0036]],
       device='cuda:0', requires_grad=True), Parameter containing:
tensor([[-0.0058, -0.0013, -0.0037,  ...,  0.0008,  0.0190, -0.0174],
        [-0.0096,  0.0277, -0.0093,  ..., -0.0246, -0.0149,  0.0090],
        [-0.0182, -0.0089,  0.0041,  ..., -0.0081,  0.0169,  0.0108],
        ...,
        [-0.0129,  0.0041, -0.0123,  ..., -0.0019,  0.0007,  0.0134],
        [ 0.0010, -0.0047,  0.0034,  ..., -0.0069, -0.0061,  0.0054],
        [ 0.0131,  0.0056, -0.0020,  ..., -0.0008, -0.0041,  0.0010]],
       device='cuda:0', requires_grad=True), Parameter containing:
tensor([0.0145, 0.0039, 0.0037,  ..., 0.0041, 0.0012, 0.0107], device='cuda:0',
       requires_grad=True), Parameter containing:
tensor([-0.0004,  0.0032, -0.0028,  ...,  0.0121, -0.0037,  0.0212],
       device='cuda:0', requires_grad=True), Parameter containing:
tensor([[-0.0024, -0.0072, -0.0013,  ...,  0.0164, -0.0134, -0.0115],
        [ 0.0133, -0.0033, -0.0029,  ..., -0.0009,  0.0165,  0.0113],
        [-0.0109, -0.0016,  0.0092,  ...,  0.0074,  0.0043, -0.0046],
        ...,
        [ 0.0008, -0.0132,  0.0030,  ..., -0.0065,  0.0033,  0.0032],
        [-0.0092,  0.0023, -0.0160,  ...,  0.0066, -0.0034,  0.0111],
        [ 0.0072, -0.0019,  0.0019,  ..., -0.0163,  0.0084, -0.0105]],
       device='cuda:0', requires_grad=True), Parameter containing:
tensor([-0.0046, -0.0093, -0.0079,  ..., -0.0136,  0.0054, -0.0116],
       device='cuda:0', requires_grad=True)], 'lr': 0.001, 'betas': (0.9, 0.999), 'eps': 1e-08, 'weight_decay': 0, 'amsgrad': False}]
```

```python
[type(p) for p in optimizer.param_groups[0]['params']]
```
```
[torch.nn.parameter.Parameter,
 torch.nn.parameter.Parameter,
 torch.nn.parameter.Parameter,
 torch.nn.parameter.Parameter,
 torch.nn.parameter.Parameter,
 torch.nn.parameter.Parameter,
 torch.nn.parameter.Parameter,
 torch.nn.parameter.Parameter,
 torch.nn.parameter.Parameter,
 torch.nn.parameter.Parameter,
 torch.nn.parameter.Parameter,
 torch.nn.parameter.Parameter]
```
- 즉, 해당 p의 attribute `grad`에 대해 `detach`하고 `zero`로 만든다.
```python
...
class Parameter(torch.Tensor):
...
```
- `nn.Parameter` 객체를 보면 `grad` attribute가 보이지 않는다.
- `nn.Parameter`는 `torch.Tensor`를 상속받는다. 그럼 torch.Tensor`에 `grad` attribute가 있을까?
- 답은 No.
- `torch.Tensor`는 `torch._C._TensorBase`를 상속받는다. 아하... 아직은 내가 팔 수 없는 영역이다.
- 공식 문서를 참고하여 설명하겠다,
- `.detach_()`는 현재의 계산 기록으로부터 해당 tensor를 분리시키고 이후에 일어나는 계산들을 추적되지 않게 한다.
- `.zero_()`는 해당 tensor를 0으로 채운다.
- 보통 method의 끝에 `_`가 붙으면 해당 객체를 변화시키는 메서드를 의미한다.

