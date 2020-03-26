# `Autograd`

## PYTORCH: TENSORS AND AUTOGRAD
- https://pytorch.org/tutorials/beginner/examples_autograd/two_layer_net_autograd.html

```python
import torch

# Declare data type and device
dtype = torch.float
device = torch.device('cuda:0') if torch.cuda.is_available() \
         else torch.device('cpu')

# N: batch size  | D_in : input dimension
# H: hidden size | D_out: output dimension
N, D_in, H, D_out = 64, 1000, 100, 10

# Create random Tensors
# Setting `requires_grad=False`: 역전파 도중 gradient가 계산되지 않게 함
# Setting `requires_grad=True` : 역전파 도중 gradient 계산을 수행
# Default: requires_grad=False
x = torch.randn(N, D_in, device=device, dtype=dtype)
y = torch.randn(N, D_out, device=device, dtype=dtype)
w1 = torch.randn(D_in, H, device=device, dtype=dtype, requires_grad=True)
w2 = torch.randn(H, D_out, device=device, dtype=dtype, requires_grad=True)

learning_rate = 1e06
for t in range(500):
    # Forward pass: W2*[relu(W1*[x]+b1)]+b2
    y_pred = x.mm(w1).clamp(min=0).mm(w2)
    # Calculate Loss, Sum((y_pred-y)**2)
    loss = (y_pred - y).pow(2).sum()
    # Use autograd to compute the backward pass
    loss.backward()
    # Since weights have `requires_grad=True`, wrap in `torch.no_grad()`
    # Alternative way: operate on weight.data and weight.grad.data
    # Recall that `tensor.data` gives a tensor that shares the storage with
    # tensor, but doesn't track history
    with torch.no_grad():
        w1 -= learning_rate * w1.grad
        w2 -= learning_rate * w2.grad
        w1.grad.zero_()
        w2.grad.zero_()
```
