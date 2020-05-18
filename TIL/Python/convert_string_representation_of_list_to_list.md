# Convert string representation of list to list

```python
>>> import ast, re
>>> data = "[['미래에셋', 'None'], ['증권', 'None']]"
>>> type(data)
<class 'str'>
>>> data = re.sub("\'None\'", "None", data)
>>> data = ast.literal_eval(data)
>>> data
[['미래에셋', None], ['증권', None]]
```
