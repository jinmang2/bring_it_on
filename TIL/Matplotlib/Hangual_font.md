#### `matplotlib` 한글 폰트가 출력될 수 있게 해주는 코드
```python
# adjust 한글 font
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
rc('font', family=font_name)
```
#### minus font
```python
plt.rcParams['axes.unicode_minus'] = False
```
