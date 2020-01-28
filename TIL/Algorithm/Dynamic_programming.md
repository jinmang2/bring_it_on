# 동적 프로그래밍

### Definition
- 세부 계산으로 나뉘어지는 하나의 큰 문제를 세부 계산 결과를 미리 구해서 저장한 후 큰 계산의 결과를 빠르게 도출해내는 문제해결 기법

### fibonacci
- 피보나치의 수학적 정의
```
for Natural number n,
    a(n) = 1 (n <= 2)
    a(n) = a(n-1) + a(n-2)
```
- 피보나치를 재귀적인 방법으로 풀면
```python
# Use recursive method,
def fib(n):
    if n < 2:
        return 1
    return fib(n-1) + fib(n-2)
```
- 일반적인 메모이제이션 알고리즘 활용, 데코레이터로 표현
```python
def memoization(func):
    memo = {}
    def wrapped(n):
        if n in memo:
            return memo[n]
        else:
            result = func(n)
            memo[n] = result
            return result
    return wrapped

@memoize
def fibonacci(n):
    return fibonacci(n-1) + fibonacci(n-2)
```
- 동적 계획법은 이러한 종류의 문제를 풀어내는 강력한 기술
- 동적 계획법의 접근은 단순한 아이디어, 코딩 역시 매우 단순
- 알고리즘이라기보다 패러다임

```
1. 탑-다운: memoization. 위 피보나치 문제와 같이 큰 계산을 작은 계산으로 나누고 작은 계산의 결과를 저장, 재사용

2. 바텀-업: 문제를 분석하여 작은 문제들이 풀려나가는 순서를 확인한 후 사소한 문제부터 플어나가기 시작.
            이 과정에서 작은 문제들은 전체 문제가 풀리기 전에 모두 풀리는 것이 보장.
```
#### 여타 다른 알고리즘들과의 차이점
- 분할정복 알고리즘에서 서브 문제들은 오버래핑되지 않음
    - 병합정렬, 퀵소트 정렬이 분할정복에 해당
- 그리디 알고리즘과도 다름
    - 특정 조건 내의 최적의 근사해를 구하는 방법
    - 별도의 수학적인 증명을 요구
    - 동적 계획법은 수학적인 유도에 의해서 만족
    
### 시스템 재귀와 동적 계획간의 냉전
- 재귀는 탑다운 방식의 해결에 자주 사용됨
- 큰 문제를 작은 문제들로 나누고 작은 문제는 같은 방식으로 계산
- 이 접근법에서 CPU시간이 점점 더 많이 쓰이고, 시간 복잡도가 증가
- 반면 동적 계획법에서는 작은 문제는 여러번 풀어지지 않으며 한번 풀린 서브 문제의 답은 전체 문제를 최적화하는데 사용
- 재귀와 동적 계획은 서브 문제가 겹치지 않는 케이스에 대해서는 거의 동일한 접근법

### 문제: 1까지의 최단 경로
```
어떤 양의 정수 n에 대해서, 이 n을 감소시키는 방법에는 여러 가지 방법이 존재.

1) 1을 뺀다.
2) n이 짝수인 경우 2로 나눈다.
3) n이 3의 배수인 경우 3으로 나눈다.

임의의 양의 정수 n에 대해 1까지 가는 최소 단계의 수를 구하면?
```
- n=10
- 탐욕 알고리즘으로 풀면 (왜 이런지는 greedy algorithm 공부하기)
```
10 (/2) -> 5 (-1) -> 4 -> 2 -> 1
```
- 10의 최단 경로는 4가 아닌 3
```
10 (-1) -> 9 (/3) -> 3 (/3) -> 1
```
- n에 대한 경로의 길이는 `1+min(Pn-1, Pn/2, Pn/3)`으로 결정
- 위 문제는 `중첩되는 서브 문제`의 성질
- 주어진 수에 대한 최적해는 주어진 수에 대한 서브 문제(n보다 작은 양의 정수들의 경로의 길이)에 의존
- memoization 풀이
```python
@memoization
def path_memo(n):
    if n < 2:
        return 0
    else:
        test = [path_memo(n-1)]
        if n % 2 == 0:
            test.append(path_memo(n/2))
        elif n % 3 == 0:
            test.append(path_memo(n/3))
        result = 1 + min(test)
        return result
```
- 위 함수의 동작 과정이 궁금하여 아래와 같이 `print`문을 찍어 함수 내부의 구조를 살펴봤다.
```python
@memoization
[ 1]    def path_memo(n):
[ 2]       print('함수호출  ', n)                      # 재귀호출 시 인자 출력
[ 3]       if n < 2:
[ 4]           return 0
[ 5]       else:
[ 6]           test = [path_memo(n-1)]
[ 7]           print(n, '\t', test, end='\t->\t')      # 처음 test를 출력
[ 8]           if n % 2 == 0:
[ 9]               test.append(path_memo(n/2))
[10]           elif n % 3 == 0:
[11]               test.append(path_memo(n/3))
[12]           print(test, end='\t')                   # 변경된 test를 출력
[13]           result = 1 + min(test)
[14]           print(result)                           # result를 출력
[15]           return result

path_memo(10)
```
```
# 주석 다 지우면 원래의 출력
# memoization 과정이 없으면 아래 cashing 부분에서 
# 이미 계산한 부분을 다시 호출하여 계산하는 불상사가 발생
# 결국에는 2의 배수, 3의 배수일 경우 재귀 호출하여 경로를 계산하고
# 작은 문제들을 풀어나가 원하는 path_memo(10)의 결과값을 도출

함수호출   10                           # 6번줄에서 재귀호출: 1
함수호출   9                            # 6번줄에서 재귀호출: 1-2
함수호출   8                            # 6번줄에서 재귀호출: 1-2-3
함수호출   7                            # 6번줄에서 재귀호출: 1-2-3-4
함수호출   6                            # 6번줄에서 재귀호출: 1-2-3-4-5
함수호출   5                            # 6번줄에서 재귀호출: 1-2-3-4-5-6
함수호출   4                            # 6번줄에서 재귀호출: 1-2-3-4-5-6-7
함수호출   3                            # 6번줄에서 재귀호출: 1-2-3-4-5-6-7-8
함수호출   2                            # 6번줄에서 재귀호출: 1-2-3-4-5-6-7-8-9
함수호출   1                            # 6번줄에서 재귀호출: 1-2-3-4-5-6-7-8-9-10
                                       # 10번 스택,
                                       # (10-3) 1 < 2 is True
                                       # (10-4) return 0, 스택 해제
                                       
2        [0]    ->      [0, 0]  1    # 9번 스택,
                                     # (9-6) test = [0] # 10번 stack의 return 값
                                     # (9-8) 2 % 2 == 0 is True
                                     # (9-9) test.append(path_memo(2/2))
                                         # n=1 cashing, 0을 반환
                                         # test = [0, 0]
                                     # (9-13) 1 + min([0, 0]) = 1
                                     # (9-14) return 1, 스택 해제
3        [1]    ->      [1, 0]  1    # 8번 스택,
                                     # (8-6) test = [1] # 9번 stack의 return 값
                                     # (8-10) 3 % 3 is True
                                     # (8-11) test.append(path_memo(3/3))
                                         # n=1 cashing, 0을 반환
                                         # test = [1, 0]
                                     # (8-13) 1 + min([1, 0]) = 1
                                     # (8-14) return 1, 스택 해제
4        [1]    ->      [1, 1]  2    # 7번 스택,
                                     # (7-6) test = [1] # 8번 stack의 return 값
                                     # (7-8) 4 % 2 == 0 is True
                                     # (7-9) test.append(path_memo(4/2))
                                         # n=2 cashing, 1을 반환
                                         # test = [1, 1]
                                     # (7-13) 1 + min([1, 1]) = 2
                                     # (7-14) return 2, 스택 해제
5        [2]    ->      [2]     3    # 6번 스택,
                                     # (6-6) test = [2] # 7번 stack의 return 값
                                     # 5는 2와 3의 배수가 아님
                                     # (6-13) 1 + min([2]) = 3
                                     # (6-14) return 3, 스택 해제
6        [3]    ->      [3, 1]  2    # 5번 스택,
                                     # (5-6) test = [3] # 6번 stack의 return 값
                                     # (5-8) 6 % 2 == 0 is True
                                     # (5-9) test.append(path_memo(6/2))
                                         # n=3 cashing, 1을 반환
                                         # test = [3, 1]
                                     # (5-13) 1 + min([3, 1]) = 2
                                     # (5-14) return 2, 스택 해제
7        [2]    ->      [2]     3    # 4번 스택,
                                     # (4-6) test = [2] # 5번 stack의 return 값
                                     # 7은 2와 3의 배수가 아님,
                                     # (4-13) 1 + min([2]) = 3
                                     # (4-14) return 3, 스택 해제
8        [3]    ->      [3, 2]  3    # 3번 스택,
                                     # (3-6) test = [3] # 4번 stack의 return 값
                                     # (3-8) 8 % 2 == 0 is True
                                     # (3-9) test.append(path_memo(8/2))
                                         # n=4 cashing, 2를 반환
                                         # test = [3, 2]
                                     # (3-13) 1 + min([3, 2]) = 3
                                     # (3-14) return 3, 스택 해제
9        [3]    ->      [3, 1]  2    # 2번 스택,
                                     # (2-6) test = [3] # 3번 stack의 return 값
                                     # (2-10) 9 % 3 == 0 is True
                                     # (2-11) test.append(path_memo(9/3))
                                         # n=3 cashing, 1을 반환
                                         # test = [3, 1]
                                     # (2-13) 1 + min([3, 1]) = 2
                                     # (2-14) return 2, 스택 해제
10       [2]    ->      [2, 3]  3    # 1번 스택,
                                     # (1-6) test = [2] # 2번 stack의 return 값
                                     # (1-8) 10 % 2 == 0 is True
                                     # (1-9) test.append(path_memo(10/5))
                                         # n=5 cashing, 3을 반환
                                         # test = [2, 3]
                                     # (1-13) 1 + min([2, 3]) = 3
                                     # (1-14) return 3, 스택 해제 후 최종 결과값
                                     
# 결국 이런거구만!
# 1을 뺀 값(이전 값)으로 가는 것이 최단인지, 2로 나눴을 시, 3으로 나눴을 시가 최단인지
# min으로 계산 후
# 해당 선택지를 취해야 하니 1을 더해준다.
# 1 + min(Pn-1, Pn/2, Pn/3)
```
- 동적 계획 풀이
```python
def path_dp(n):
    paths = [0, 0] + [0] * n
    #        ^0 ^1   ..... n
    # path[1] = 0
    for i in range(2, n+1):
        paths[i] = paths[i-1] + 1
        if i % 2 == 0:
            paths[i] = min((paths[i], 1 + paths[i//2]))
        elif i % 3 == 0:
            paths[i] = min((paths[i], 1 + paths[i//3]))
    return paths[n]
```
```python
# 시간비교

# path_memo
for i in range(2, 11):
    %timeit path_memo(i)
    
>>> 128 ns ± 0.259 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
>>> 129 ns ± 1.08 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
>>> 129 ns ± 0.441 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
>>> 130 ns ± 0.378 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
>>> 128 ns ± 0.553 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
>>> 129 ns ± 1.04 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
>>> 129 ns ± 0.251 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
>>> 128 ns ± 0.604 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
>>> 128 ns ± 1.03 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

# path_dp
for i in range(2, 11):
    %timeit path_dp(i)
    
>>> 806 ns ± 2.43 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
>>> 1.17 µs ± 2.72 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
>>> 1.51 µs ± 4.55 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
>>> 1.66 µs ± 8.58 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
>>> 2.01 µs ± 29.7 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
>>> 2.16 µs ± 14.1 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
>>> 2.49 µs ± 7.4 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
>>> 2.85 µs ± 8.28 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
>>> 3.16 µs ± 18.5 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
```
### 문제: 가장 긴 증가하는 부분 수열
```
주어진 수열에 대해 그 부분 수열 중, 각 항이 증가하는 순서로 구성된 가장 긴 부분 수열을 찾아라
```
- 가장 평이한 로직은 다음 항이 이전 항보다 크면 부분 수열에 추가하는 식으로 검사
- 최악의 경우 O(n^2)의 시간 복잡도를 가짐
- 이는 수열의 맨 뒤에서부터 앞의 항이 뒤의 항보다 큰 경우에서 시작하여(증가하는 부분 수열의 끝)
- 앞으로 나가면서 길이값을 1씩 늘려나가고, 다시 앞의 항이 더 큰 경우를 만나면 0으로 초기화하는 방법을 사용하면
- O(n)의 시간 복잡도로 줄일 수 있다.
```python
def LIS(aList):
    _length = len(aList)
    lis = [0] + [0] * _length
    for i in range(_length-2, 0, -1):
        if aList[i] < aList[i+1]:
            lis[i] = lis[i+1] + 1
    max_index = lis.index(max(lis))
    return aList[max_index:max_index+lis[max_index]+1]
    
a = [8, 3, 2, 4, 5, 6, 2, 7, 1, 2, 4, 7, 8, 9, 7]
l = len(a)
lis = [0] * (l + 1)

RANGE = range(l-2, 0, -1)
for i in RANGE:
    if i == l-2:
        print('i\t a[i]\t a[i+1]\t cond\t lis')
    print(i, '\t', a[i], '\t', a[i+1], end='')
    if a[i] < a[i+1]:
        lis[i] = lis[i+1] + 1
        BOOL = True
    else:
        BOOL = False
    print('\t', BOOL, '\t', lis)
    
>>> i        a[i]    a[i+1]  cond    lis
>>> 13       9       7       False   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>>> 12       8       9       True    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
>>> 11       7       8       True    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0]
>>> 10       4       7       True    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 1, 0, 0, 0]
>>> 9        2       4       True    [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 2, 1, 0, 0, 0]
>>> 8        1       2       True    [0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 0, 0, 0]
>>> 7        7       1       False   [0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 3, 2, 1, 0, 0, 0]
>>> 6        2       7       True    [0, 0, 0, 0, 0, 0, 1, 0, 5, 4, 3, 2, 1, 0, 0, 0]
>>> 5        6       2       False   [0, 0, 0, 0, 0, 0, 1, 0, 5, 4, 3, 2, 1, 0, 0, 0]
>>> 4        5       6       True    [0, 0, 0, 0, 1, 0, 1, 0, 5, 4, 3, 2, 1, 0, 0, 0]
>>> 3        4       5       True    [0, 0, 0, 2, 1, 0, 1, 0, 5, 4, 3, 2, 1, 0, 0, 0]
>>> 2        2       4       True    [0, 0, 3, 2, 1, 0, 1, 0, 5, 4, 3, 2, 1, 0, 0, 0]
>>> 1        3       2       False   [0, 0, 3, 2, 1, 0, 1, 0, 5, 4, 3, 2, 1, 0, 0, 0]
#                                                             _ is max index!! and contents is 5.

max_index = lis.index(max(lis))
max_index
>>> 8
lis[max_index]
>>> 5
a
>>> [8, 3, 2, 4, 5, 6, 2, 7, 1, 2, 4, 7, 8, 9, 7]
#                            _________________ Here!! 1 to 9, 5 steps
a[max_index:max_index+lis[max_index]+1]
>>> [1, 2, 4, 7, 8, 9]
```


출처: https://soooprmx.com/archives/5515
