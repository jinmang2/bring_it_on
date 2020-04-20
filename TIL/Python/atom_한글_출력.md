# 아톰에서 파이썬 스크립트 실행시 한글 깨짐현상 잡는 꿀팁

#### 출처: https://mrcoding.tistory.com/entry/아톰에서-파이썬-스크립트-실행시-한글-깨짐현상-잡는-꿀팁

```python
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
```
