# `.squeeze()` and `.unsqueeze()`
- `.squeeze()`: 차원의 원소가 1인 차원 제거
- `.unsqueeze()`: 차원을 삽입

```python
import torch

x = torch.randn((5, 2, 1, 1, 3))
x.squeeze().shape
>>> torch.Size([5, 2, 3])
x.squeeze(dim=2).shape
>>> torch.Size([5, 2, 1, 3])
x.unsqueeze(dim=1).shape
>>> torch.Size([5, 1, 2, 1, 1, 3])
x.unsqueeze().shape
>>> TypeError: unsqueeze() missing 1 required positional arguments: "dim"
```
