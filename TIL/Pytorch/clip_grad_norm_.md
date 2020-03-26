# `clip_grad_norm_`
- Gradient Clipping
    - https://dhhwang89.tistory.com/90
    - https://kh-kim.gitbook.io/natural-language-processing-with-pytorch/00-cover-6/05-gradient-clipping
- Frobenius Norm을 계산하고 max_norm / (Frobenius + epsilon)이 1보다 작을 경우 해당 grad에 곱해줌
```python
import torch

torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
```

- source code
```python
import warnings
import torch
import math

inf = math.inf

def clip_grad_norm_(parameters, max_norm, norm_type=2):
    if isinstance(parameters, torch.Tensor):
        # 입력된 parameter가 Tensor객체라면 list로 바꿈
        parameters = [parameters]
    # 각 parameter의 `grad` attribute가 None이 아닌 객체만 수집
    parameters = list(filter(lambda p: p.grad is not None, parameters))
    # 입력받은 최대 노름값 float로 변환
    max_norm = float(max_norm)
    # 입력받은 노름 타입 float로 변환
    norm_type = float(norm_type)
    # If p is infinite,
    if norm_type == inf:
         # then calculate maximum norm L = max(|x1|, |x2|, |x3|, ..., |xn|)
        total_norm = max(p.grad.data.abs().max() for p in parameters)
    # If p finite,
    else:
        # then calculate Frobenius Norm with p s.t not infinite
        total_norm = 0
        for p in parameters:
            # Calc norm
            param_norm = p.grad.data.norm(norm_type)
            # Add scalar(norm) ** p
            total_norm += param_norm.item() ** norm_type
        total_norm = max_norm / (total_norm + 1e-6)
    # Calc clip_coef as follow:
    clip_coef = max_norm / (total_norm + 1e-6) # scalar
    if clip_coef < 1:
        for p in parameters:
            p.grad.data.mul_(clip_coef)
    return total_norm
    
```
