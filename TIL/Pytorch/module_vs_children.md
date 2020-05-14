```python
import math
import torch
import torch.nn as nn
import torch.nn.functional as F

activations = [
        'sigmoid', 
        'tanh', 
        'relu', 
        'rrelu', 
        'elu',
        'hardtanh',
        'celu',
        'selu',
        'glu',
        'gelu',
        'hardshrink',
        'leaky_relu'
        'logsigmoid',
        'softplus',
        'softshrink',
        'prelu',
        'softsign',
        'tanhshrink',
        'softmin',
        'softmax',
        'log_softmax',
    ]

class MyLinear(nn.Module):

    __activations__ = activations
    __constants__ = ['bias', 'in_features', 'out_features']

    def __init__(self, input_dim, output_dim, bias=True, activation='sigmoid'):
        super().__init__()
        self.in_features = input_dim
        self.out_features = output_dim
        self.activation = None
        if activation.lower() in self.__activations__:
            setattr(self, 'activation', getattr(F, activation))
        else:
            raise Exception(f"Unknown activation function: {activation}")
        self.weight = nn.Parameter(torch.Tensor(output_dim, input_dim))
        if bias:
            self.bias = nn.Parameter(torch.Tensor(output_dim))
        else:
            # self.register_backward_hook('bias', None)
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self,
                         init_weight='he', 
                         init_bias='uniform',
                         a=math.sqrt(5),
                         gain=1.):
        if init_weight.lower() in ['xavier', 'glorot']:
            nn.init.kaiming_uniform(self.weight, a=math.sqrt(5))
        elif init_weight.lower() in ['kaiming', 'he']:
            nn.init.xavier_uniform_(self.weight, gain=1.)
        else:
            raise ValueError(f"Unknown init_weight: {init_weight}")
        self.init_weight = init_weight
        if self.bias is not None:
            if init_bias == 'uniform':
                fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
                bound = 1 / math.sqrt(fan_in)
                nn.init.uniform_(self.bias, -bound, bound)
            elif init_bias in ['zero', 'zeros']:
                nn.init.zeros_(self.bias)
            elif isinstance(init_bias, int):
                self.bias.data.fill_(init_bias)

    def forward(self, input):
        output = input.matmul(self.weight.T)
        if self.bias:
            output += self.bias
        if self.activation:
            output = self.activation(output)
        return output

    def extra_repr(self):
        return 'in_features={}, out_features={}, bias={}'.format(
            self.in_features, self.out_features, self.bias is not None
        )

class Model(nn.Module):

    def __init__(self,
                 in_features,
                 out_features,
                 first=False,
                 couple=False,
                 dropout_p=0.0):
        super().__init__()
        self.first = first
        self.couple = couple
        if first:
            self.W_H = Linear(in_features, out_features, bias=False)
            self.W_T = Linear(in_features, out_features, bias=False)
            if not couple:
                self.W_C = Linear(in_features, out_features, bias=False)
        self.R_H = Linear(in_features, out_features, bias=True)
        self.R_T = Linear(in_features, out_features, bias=True)
        if not couple:
            self.R_C = Linear(in_features, out_features, bias=True)


model = Model(10, 20, True, False)
# 정상적으로 동작!
for child in model.children():
    print(child)
    child.reset_parameters('kaiming', -1)
# 에러 발생!
"""
예외가 발생했습니다.AttribueError
'Model' object has no attribute 'reset_parameters'
"""
for module in model.modules():
    print(module)
    module.reset_parameters('kaiming', -1)
print(list(model.parameters()))
```

# 에러 발생의 이유?
- `nn.Module.children`은 child만 저장
- `nn.Module.modules`는 자기 자신도 저장!!
