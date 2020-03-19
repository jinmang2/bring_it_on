# Contiguous vs non-contiguous tensor
단순한 차이!
- memory가 `contiguously`하게 저장되어 있느냐 아니느냐
---
```python
x = torch.arange(12).view(4, 3)

print(x)
>>> tensor([[ 0,  1,  2],
>>>         [ 3,  4,  5],
>>>         [ 6,  7,  8],
>>>         [ 9, 10, 11]])

print(x.stride())
>>> (3, 1)
```
위의 tensor는 메모리에 아래와 같이 저장되어 있다.
- `[0, 1, 2, 3, ..., 11]`
- 여기서 0th axis는 3개 단위로 끊기고 1st axis는 1개 단위로 끊긴다는 이야기!

Tensor를 `transpose`시켜 다시 살펴보자.
```python
y = x.t()

print(y)
>>> tensor([[ 0,  3,  6,  9],
>>>         [ 1,  4,  7, 10],
>>>         [ 2,  5,  8, 11]])

print(y.stride())
>>> (1, 3)
```
자세히 보면, 원래 `stride`를 우리가 직접 계산한다고 생각하면
- `shape`이 `(3, 4)`이므로
- `stride`는 `(4, 1)`이 되겠지?

그러나 `transpose`된 `stride`는 `(1, 3)`으로 출력되고 있다.

이게 무슨 소리냐? 0th dim으로 움직이는데는 step 1개, 1st dim으로 움직이는데는 step이 3개 필요하다는 소리이다.

즉, 데이터는 아래와 같이 저장되어 있음을 의미한다.
- `[0, 1, 2, 3, ..., 11]`
- x와 똑같다! `stride`만 달라졌을 뿐...

`transpose`는 빠르게 수행되어 `view`를 빠르게 해줄 수 있었지만... 실제 메모리 상 변화는 없다는 말!
- 즉, `non-contiguous`하다!!

한번 아래의 명령어를 찍어보자.
```python
print(x.is_contiguous())
>>> True

print(y.is_contiguous())
>>> False
```
x는 contiguous하게 메모리에 저장되어 있기 때문에 `is_contiguous()`메서드를 통해 contiguous한지 살펴보면 `True`인 것을 확인할 수 있다.

그러나 y는 위에서 본 것과 같이 `[0, 3, 6, 9, 1, ..., 11]`과 같이 저장되있지 않지 않는가? 즉 `is_contiguous()`메서드를 통해 확인하면 contiguous하게 저장되어 있지 않음을 확인할 수 있다.

**그렇다면, 무엇이 문제인가?**

우리가 단순히 보기에는 문제될 일이 없어보이지만, 연산을 수행하려고하면 에러가 발생한다.

```python
y = y.view(-1)
>>> RuntimeError: view size is not compatible with input tensor's size and stride (at least one dimension spans across two contiguous subspaces). Use .reshape(...) instead.
```

그렇다면, `view` 등의 연산을 하기 위해서는 어떻게 해야하는가?
- `view`를 호출하기 전에 `.contiguous()` 메서드를 호출하라.

```python
y = y.contiguous()
print(y.stride())
>>> (4, 1)

y = y.view(-1)
# No error occurs
```
`stride`를 보면 처음에 계산한 `(4, 1)`로 메모리에 저장된 것을 확인할 수 있다.
---


## 출처:
- https://github.com/jinmang2/bring_it_on/blob/master/TIL/Pytorch/stride.md
- https://discuss.pytorch.org/t/contigious-vs-non-contigious-tensor/30107
- https://stackoverflow.com/questions/48915810/pytorch-contiguous
- https://m.blog.naver.com/PostView.nhn?blogId=chrhdhkd&logNo=221477295040&proxyReferer=https%3A%2F%2Fwww.google.com%2F
