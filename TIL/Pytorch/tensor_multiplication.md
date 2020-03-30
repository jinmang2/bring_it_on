# Tensors multiplication 3D*2D

```python
import torch

A = torch.randn(4, 10, 128)
B = torch.randn(4, 10)

res1 = torch.mm(A.view(-1, 4), B).view(128, 10, 10)
res2 = A.permute(2, 1, 0).matmul(B)

print(res1.shape, res2.shape)
>>> torch.Size([128, 10, 10]), torch.Size([128, 10, 10])

print(torch.sum(res1 - res2)) # not same. why?
>>> torch(-20.6725)
```

- 정수로 어떻게 연산이 진행되는지 체크
```python
A = torch.arange(0, 24).view(3, 2, 4)
B = torch.LongTensor([[1, 2], [3, 4], [4, 5]])

print(A.shape, B.shape)
>>> torch.Size([3, 2, 4]), torch.Size([3, 2])

print(A)
>>> tensor([[[ 0,  1,  2,  3],
>>>          [ 4,  5,  6,  7]],
>>> 
>>>         [[ 8,  9, 10, 11],
>>>          [12, 13, 14, 15]],
>>> 
>>>         [[16, 17, 18, 19],
>>>          [20, 21, 22, 23]]])

print(B)
>>> tensor([[1, 2],
>>>         [2, 1],
>>>         [3, 3]])

# First case,
print(A.view(-1, A.size(0)))
>>> tensor([[ 0,  1,  2],
>>>         [ 3,  4,  5],
>>>         [ 6,  7,  8],
>>>         [ 9, 10, 11],
>>>         [12, 13, 14],
>>>         [15, 16, 17],
>>>         [18, 19, 20],
>>>         [21, 22, 23]])

# A.shape == (2*4, 3), B.shape == (3, 2)
# result shape is (8, 2)
res1 = torch.mm(A.view(-1, A.size(0)), B)
print(res1)
>>> tensor([[  8,   7],     # [row_A0 * col_B0, row_A0 * col_B1]
>>>         [ 26,  25],     # [row_A1 * col_B0, row_A1 * col_B1]
>>>         [ 44,  43],     # [row_A2 * col_B0, row_A2 * col_B1]
>>>         [ 62,  61],     # [row_A3 * col_B0, row_A3 * col_B1]
>>>         [ 80,  79],     # [row_A4 * col_B0, row_A4 * col_B1]
>>>         [ 98,  97],     # [row_A5 * col_B0, row_A5 * col_B1]
>>>         [116, 115],     # [row_A6 * col_B0, row_A6 * col_B1]
>>>         [134, 133]])    # [row_A7 * col_B0, row_A7 * col_B1]

print(res1.view(2, 4, 2))
>>> tensor([[[  8,   7],     # [ [row_A0 * col_B0, row_A0 * col_B1]
>>>          [ 26,  25],     #   [row_A1 * col_B0, row_A1 * col_B1]
>>>          [ 44,  43],     #   [row_A2 * col_B0, row_A2 * col_B1]
>>>          [ 62,  61]],    #   [row_A3 * col_B0, row_A3 * col_B1] ]
>>> 
>>>         [[ 80,  79],     # [ [row_A4 * col_B0, row_A4 * col_B1]
>>>          [ 98,  97],     #   [row_A5 * col_B0, row_A5 * col_B1]
>>>          [116, 115],     #   [row_A6 * col_B0, row_A6 * col_B1]
>>>          [134, 133]]])   #   [row_A7 * col_B0, row_A7 * col_B1] ]

# Second case,
print(A.permute(2, 1, 0)) # transpose to (4, 2, 3)
>>> tensor([[[ 0,  8, 16],
>>>          [ 4, 12, 20]],
>>> 
>>>         [[ 1,  9, 17],
>>>          [ 5, 13, 21]],
>>> 
>>>         [[ 2, 10, 18],
>>>          [ 6, 14, 22]],
>>> 
>>>         [[ 3, 11, 19],
>>>          [ 7, 15, 23]]])

print(A.permute(2, 1, 0).matmlu(B))
>>> tensor([[[ 64,  56],
>>>          [ 88,  80]],
>>> 
>>>         [[ 70,  62],
>>>          [ 94,  86]],
>>> 
>>>         [[ 76,  68],
>>>          [100,  92]],
>>> 
>>>         [[ 82,  74],
>>>          [106,  98]]])
```

## 왜 다를까?
`view` 메서드의 동작구조를 알아야 한다.
tensor는 아래와 같이 저장된다.
```python


```
