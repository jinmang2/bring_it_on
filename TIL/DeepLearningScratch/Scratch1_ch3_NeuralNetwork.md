# Chapter 3. Neural Network
### Remind Perceptron
- y = 1 if b + w1x1 + w2x2 > 0 else 0
- b: bias, 뉴런이 얼마나 쉽게 활성화되느냐를 제어
- w: weight, 각 신호의 영향력을 제어
- y = Step(b + w1x1 + w2x2)

### Activation function
- 입력 신호의 총합이 활성화를 일으키는지를 정하는 역할 수행
- 뉴런, 노드는 동일한 용어로 교재에서는 활용

#### Step
```python
def step(x):
    return (x > 0).astype(np.int)
```

#### Sigmoid
```python
def sigmiod(x):
    return 1 / (1 + np.exp(-x))
```
#### ReLU(Rectified Linear Unit)
```python
def relu(x):
    return np.maximum(0, x)
```

### Non-Linear function
- 함수에 어떠한 인풋을 넣어줬을 때 출력이 입력의 상수배만큼 변하는 함수를 **선형 함수**라고 일컬음
- 직관적으로 생각했을 때, 하나의 직선으로 설명할 수 없는 함수를 **비선형 함수**라고 부름
- 선형함수를 사용했을 시, 층을 깊게 쌓는 이유가 없음. (a = c^3)
