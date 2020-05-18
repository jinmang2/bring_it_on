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
