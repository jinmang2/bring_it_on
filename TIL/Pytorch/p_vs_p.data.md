```python
import torch

...

# gradient descent를 사용하여 가중치를 수동으로 갱신하는 코드 1
with torch.no_grad():
    w1 -= learning_rate * w1.grad
    w2 -= learning_rate * w2.grad

    w1.grad.zero_()
    w2.grad.zero_()

# gradient descent를 사용하여 가중치를 수동으로 갱신하는 코드 2
w1 -= learning_rate * w1.grad.data
w2 -= learning_rate * w2.grad.data

w1.grad.data.zero_()
w2.grad.data.zero_()
```

### 출처
- https://tutorials.pytorch.kr/beginner/examples_autograd/two_layer_net_autograd.html
