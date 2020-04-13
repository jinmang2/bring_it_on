# 아하... 젠장
- 자 아래 예제를 보고 오늘의 실수를 반성하자

```python
>>> # vocab은 한국어 단어사전
>>> # init_token=='<bos>'의 값은 2라고 가정
>>> bsz = 3
>>> output = [[vocab[init_token]]] * bsz
>>> output
[[1], [1], [1]]

>>> output.extend([1,2,3,4])
>>> output
[[1], [1], [1], 1, 2, 3, 4]

>>> output = [[vocab[init_token]]] * bsz # reset
>>> output[0].extend([1,2,3,4]) # 기대하는바는 0번째 list에만 추가되는 것이지만
>>> output # 짜라란! 전부 추가되지롱~
[[1, 1, 2, 3, 4], [1, 1, 2, 3, 4], [1, 1, 2, 3, 4]]
```
