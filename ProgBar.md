## Link
- https://m.blog.naver.com/PostView.nhn?blogId=samsjang&logNo=220982297456&proxyReferer=https%3A%2F%2Fwww.google.com%2F

## 어떤 역할?
- tqdm, for loop에서 진행 경과를 한 줄 출력으로 처리해주는 클래스

## 코드는?
```python
class ProgBar():
    def __init__(self, step=100):
        self.step = int(step / 20)
        self.count = 1
        self.progress = 0
    def update(self):
        if self.count % self.step == 0:
            self.progress += 1
            print('\r[{:s}{:s}]'.format('#'*self.progress, ' ' * (20 - self.progress)), end='')
        self.count += 1
```
