```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math


import time
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('\'{:s}\'  {:2.2f} ms  {:2.2f} sec  {:2.2f} min  {:2.2f} hour'.format(
                  method.__name__, (te - ts) * 1000, (te - ts), (te - ts) / 60, (te - ts) / 3600))
        return result
    return timed


class MyLinear(nn.Module):

    __constants__ = ['bias', 'in_features', 'out_features']

    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = nn.Parameter(torch.Tensor(out_features, in_features))
        if bias:
            self.bias = nn.Parameter(torch.Tensor(out_features))
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / math.sqrt(fan_in)
            nn.init.uniform_(self.bias, -bound, bound)
    @timeit
    def forward(self, input):
        # num_batches = input.size(0)
        # res = []
        # for i in range(num_batches):
        #     affine = torch.mm(self.weight, input[i].T).T + self.bias
        #     res.append(affine)
        # output = torch.cat([i.view(1, *i.size()) for i in res]).contiguous()
        # return output
        return input.matmul(self.weight.T) + self.bias

    def extra_repr(self):
        return 'in_features={}, out_features={}, bias={}'.format(
            self.in_features, self.out_features, self.bias is not None
        )

input = torch.randn((32, 10, 170000))

torch_linear = nn.Linear(170000, 1000)
my_linear    =  MyLinear(170000, 1000)
my_linear.weight = torch_linear.weight
my_linear.bias   = torch_linear.bias

@timeit
def forward(self, input):
    return F.linear(input, self.weight, self.bias)

setattr(torch_linear.__class__, 'forward', forward)

a = torch_linear(input)
b = my_linear(input)
```
