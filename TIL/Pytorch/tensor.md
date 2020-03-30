# What is Tensor?
## Import Library
```python
import torch
```

## 1D Tensor
```python
X = torch.Tensor([1, 2])
X
>>> tensor([1., 2.])

X.size()
>>> torch.size([2])

X.stride()
>>> (1,)

X.is_contiguous()
>>> True
```
## 2D Tensor
```python
X = torch.Tensor(
    [[1, 2],
     [3, 4],
     [5, 6]]
)
X
>>> tensor([[1., 2.],
>>>         [3., 4.],
>>>         [5., 6.]])

X.size()
>>> torch.Size([3, 2])

X.stride()
>>> (2, 1)

X.is_contiguous()
>>> True
```

## 3D Tensor
```python
X = torch.Tensor(
    [[[1, 2, 3],
      [2, 3, 4],
      [3, 4, 5],
      [0, 0, 0]],
      
     [[4, 5, 6],
      [6, 7, 8],
      [7, 8, 9],
      [0, 0, 0]]]
)
X
>>> tensor([[[1., 2., 3.],
>>>          [2., 3., 4.],
>>>          [3., 4., 5.]
>>>          [0., 0., 0.]],
>>> 
>>>         [[4., 5., 6.],
>>>          [6., 7., 8.],
>>>          [7., 8., 9.]
>>>          [0., 0., 0.]]])

X.size()
>>> torch.Size(2, 4, 3)

X.stride()
>>> (12, 3, 1)
```
