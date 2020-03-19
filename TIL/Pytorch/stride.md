# What is `stride`?
- `strides`는 주어진 dimension에서 한 요소에서 다른 요소로 가는데 필요한 `steps (or jumps)`의 수
- `computer memory`에서 `data`는 memory의 `contiguous block`에 선형적으로 정렬되있음
- `view`는 단순히 `repr`일뿐!!
    - `str`과 `repr`의 차이라고 생각하면 된다.

```python
# 2D Tensor
tensor = torch.arange(1, 16).reshape(3, 5)
print(tensor)
>>> tensor([[ 1,  2,  3,  4,  5],
>>>         [ 6,  7,  8,  9, 10],
>>>         [11, 12, 13, 14, 15]])

# get the strides
print(tensor.stride())
>>> (5, 1)

x = torch.arange(24).view(2, 3, 4)
print(x)
>>> tensor([[[ 0,  1,  2,  3],
>>>          [ 4,  5,  6,  7],
>>>          [ 8,  9, 10, 11]],
>>> 
>>>         [[12, 13, 14, 15],
>>>          [16, 17, 18, 19],
>>>          [20, 21, 22, 23]]])

print(x.stride())
>>> (12, 4, 1)
```
- 이를 계산하는 방법은 다음과 같다.
```
view   = (v_{1}, 
          v_{2}, 
          ...,
          v_{n-1},
          v_{n})

stride = (v_{2}*v_{3}*...*v_{n},
          v_{3}*...*v_{n},
          ...,
          v_{n},
          1)
```

## 무엇을 의미하는가?
처음의 예제를 다시 보자.
```python
# 2D Tensor
tensor = torch.arange(1, 16).reshape(3, 5)
print(tensor)
>>> tensor([[ 1,  2,  3,  4,  5],
>>>         [ 6,  7,  8,  9, 10],
>>>         [11, 12, 13, 14, 15]])

# get the strides
print(tensor.stride())
>>> (5, 1)
```

tuple `(5, 1)`이 의미하는 바는
- 0th dimension/axis를 따라 탐색하기 위해, (`1`에서 `6`으로 가는 길!) `5` steps이 필요하다.
- 1st dimension/axis를 따라 탐색하기 위해, (`7`에서 `8`로 가는 길!) `1` step이 필요하다.

## 왜 써?
간단한 이유가 존재.
- `How can we store/read/access the elements in the (sparse) tensor most efficiently?`

sparse tensor의 경우, 우리는 `non-zero values`와 그 `indices`만 저장하면 그만

## 출처:
- https://stackoverflow.com/questions/56659255/what-does-layout-torch-strided-mean
