# `torch.clamp`
- set upper bound and lower bound on tensor.

```python
import torch

x = torch.randn((5, 2))
x
>>> tensor([[ 1.4075,  1.4899],
>>>         [ 0.1220, -0.8169],
>>>         [-0.0489, -0.1953],
>>>         [-0.6971,  1.6134],
>>>         [-1.8344,  0.1008]])

torch.clamp(x, -0.5, 0.5)
>>> tensor([[ 0.5000,  0.5000],
>>>         [ 0.1220, -0.5000],
>>>         [-0.0489, -0.1953],
>>>         [-0.5000,  0.5000],
>>>         [-0.5000,  0.1008]])
```
