# 파이썬 데코레이터를 통한 memoization

### 피보나치 수열을 memoization을 통해 성능 개선시키기
```python
def fib(n):
    if n in (1, 2):
        return 1
    return fib(n-1) + fib(n-2)
```
- 이 코드를 사용하여 수열의 64번째 항을 구하면 재귀 호출을 2^64-1번 해야한다.
- memoization을 활용하여 성능 개선을 해보자.
- 이를 cashing, memoization이라고 부른다.
```python
memo = dict()
def fib2(n):
    if n in memo:
        return memo[n]
    if n in (1, 2):
        memo[n] = 1
        return 1
    result = fib2(n-1) + fib2(n-2)
    memo[n] = result
    return result
```
- 한번 계산한 결과를 재계산할 필요가 없고 이를 통해 재귀 호출을 막을 수 있어 64번만 계산하면 된다.
- 그러나 전역변수 memo를 사용해야하는 불편함이 있다.
- 파이썬의 데코레이터(함수를 인자로 받는 closure)는 closure같이 부모함수의 스코프에서 특정 값을 캡처할 수 있다.
```python
def momoize(func):
    tempMemo = dict()
    def wrapped(n):
        if n in tempMemo:
            return tempMemo[n]
        result = func(n)
        tempMemo[n] = result
        return result
    return wrapped
    
fib = memoize(fib)
fib(64)
```
- 함수 `memoize`는 함수를 인자로 받고 다른 함수를 반환
- 반환되는 함수는 힘시 사전에 계산 결과를 기록하고, 계산한 이력이 있으면 재계산없이 해당 내용을 그대로 리턴
- 이 때 이 계산 결과를 캐시하는 객체는 부모함수인 `memoize`의 스코프에 있는 객체
- 함수 `memoize`는 호출될 때마다 새로운 함수를 반환하는데, 이 반환되는 함수는 자신이 리턴되는 시점에 캡처한 `tempMemo` 객체에 대한 참조를 가짐
- 즉, 부모함수인 `memoize`의 사이클은 종료되지만 해당 객체는 파괴되지 않고 계속 유지.
- 이 말인 즉슨 이 함수를 계속 사용하는 한, 한 번 계산된 결과는 계속해서 캐싱됨
```python
@memoize
def fib2(n):
    if n in (1, 2):
        return 1
    return fib2(n-1) + fib2(n-2)
```
- 저자는 아래 두 제약을 언급한다.
    1) 함수는 1개의 인자만 받으며
    2) 그 인자는 사전의 키가 될 수 있는 객체여야 한다. (리스트는 될 수 없다.)
- 2)는 동의하지만 1)같은 경우는 asterisk로 더 추가할 수 있지 않을까..?
- 속도를 비교한 것은 아래와 같다.
```python
%timeit fib(5)
>>> 770 ns ± 6.75 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
%timeit fib(10)
>>> 9.23 µs ± 76.7 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
%timeit fib(15)
>>> 104 µs ± 1 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
%timeit fib(20)
>>> 1.16 ms ± 9.8 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
%timeit fib(25)
>>> 12.9 ms ± 89.7 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
%timeit fib(30)
>>> 144 ms ± 1.41 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
%timeit fib(35)
>>> 1.61 s ± 11.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each

%timeit fib2(5)
>>> 109 ns ± 1.46 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
%timeit fib2(10)
>>> 111 ns ± 0.454 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
%timeit fib2(15)
>>> 110 ns ± 0.645 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
%timeit fib2(20)
>>> 109 ns ± 1.19 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
%timeit fib2(25)
>>> 109 ns ± 0.83 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
%timeit fib2(30)
>>> 110 ns ± 0.577 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
%timeit fib2(35)
>>> 110 ns ± 0.739 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

%timeit fib2(256)
>>> 113 ns ± 0.694 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

fib2(202001)
```
```
---------------------------------------------------------------------------
RecursionError                            Traceback (most recent call last)
<ipython-input-26-e9dfcdbc2f92> in <module>
----> 1 fib2(202001)

<ipython-input-7-7febea742704> in wrapped(n)
      4         if n in tempMemo:
      5             return tempMemo[n]
----> 6         result = func(n)
      7         tempMemo[n] = result
      8         return result

<ipython-input-8-e59631240d10> in fib2(n)
      3     if n in (1, 2):
      4         return 1
----> 5     return fib2(n-1) + fib2(n-2)
      6

... last 2 frames repeated, from the frame below ...

<ipython-input-7-7febea742704> in wrapped(n)
      4         if n in tempMemo:
      5             return tempMemo[n]
----> 6         result = func(n)
      7         tempMemo[n] = result
      8         return result

RecursionError: maximum recursion depth exceeded in comparison
```

출처: https://soooprmx.com/archives/5149
