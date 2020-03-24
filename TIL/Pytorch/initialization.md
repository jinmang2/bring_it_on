```python

@torch.no_grad()
def init_weights(m):
    print(m)
    if type(m) == nn.Linear:
        nn.init.xavier_uniform(m.weight)
        m.bias.data.fill_(0.01)
        
```
