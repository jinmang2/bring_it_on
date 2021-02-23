```python
import inspect

class T:
    def forward(self, x, s, e, j, y):
        return 10
      
t = T()
signature = inspect.signature(t.forward)
list(signature.parameters().keys())
```
```
['x', 's', 'e', 'j', 'y']
```
