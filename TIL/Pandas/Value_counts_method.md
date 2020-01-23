# `pandas.Series.value_counts`

### parameters
- `normalize`: _boolean, default False_<br>
    If True then the object returned will contain the relative frequencies of the unique values.

- `sort` : _boolean, default True_<br>
    Sort by frequencies.

- `ascending` : _boolean, default False_<br>
    Sort in ascending order.

- `bins` : _integer, optional_<br>
    Rather than count values, group them into half-open bins, a convenience for pd.cut, only works with numeric data.

- `dropna` : _boolean, default True_<br>
    Don’t include counts of NaN.
    
### Usage
```python
df.업무선택.value_counts()
```
```
07.자동차보상       164
06.자동차보험       148
10.홈페이지/모바일     37
04.장기보험금청구      19
08.장기보험         16
09.고객            4
00.공통            2
01.보험계약조회        1
Name: 업무선택, dtype: int64
```
```python
df.업무선택.value_counts(normalize=True)
```
```
07.자동차보상       0.419437
06.자동차보험       0.378517
10.홈페이지/모바일    0.094629
04.장기보험금청구     0.048593
08.장기보험        0.040921
09.고객          0.010230
00.공통          0.005115
01.보험계약조회      0.002558
Name: 업무선택, dtype: float64
```
