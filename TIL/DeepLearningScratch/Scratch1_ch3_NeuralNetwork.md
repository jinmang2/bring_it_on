# Chapter 3. Neural Network
- 핵심: 신경망에서의 계산을 행렬의 계산으로 정리할 수 있다.
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
def sigmoid(x):
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

### 다차원 배열 계산
```python
import numpy as np

# 1차원 배열
A = np.array([1, 2, 3, 4])
np.dim(A)
>>> 1
A.shape
>>> (4,)
A.shape[0] # tuple 객체의 0번째 인덱스에 접근
>>> 4

# 2차원 배열
B = np.array([[1,2],[3,4],[5,6]])
np.dim(B)
>>> 2
B.shape
>>> (3, 2)

# 행렬의 곱
A = np.array([[1,2],[3,4]])
B = np.array([[5,6],[7,8]])

np.dot(A, B)
>>> array([[19, 22],
>>>        [43, 50]])
A.dot(B)
>>> array([[19, 22],
>>>        [43, 50]])
A @ B
>>> array([[19, 22],
>>>        [43, 50]])
A * B # element-wise multiplication
>>> array([[ 5, 12],
>>>        [21, 50]])
```

### Implement 3-layers NN
```python
def init_network():
    # 네트워크는 가중치와 편향의 값을 내부에 저장하고 있다.
    network = {}
    network['W1'] = np.array([[0.1, 0.3, 0.5], [0.2, 0.4, 0.6]])
    network['b1'] = np.array([0.1, 0.2, 0.3])
    network['W2'] = np.array([[0.1, 0.4], [0.2, 0.5], [0.3, 0.6]])
    network['b2'] = np.array([0.1, 0.2])
    network['W3'] = np.array([[0.1, 0.3], [0.2, 0.4]])
    network['b3'] = np.array([0.1, 0.2])
    
    return network
    
def identity_function(x):
    return x

def forward(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']
    
    # 실제로 중간에 sigmoid를 활성화 함수로 사용하게 되면 vanishing gradient 문제에 직면하게 된다.
    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(a1, W2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, W3) + b3
    y = identity_function(a3)
    
    return y
    
network = init_network()
x = np.array([1.0, 0.5])
y = forward(network, x)
prnit(y) # [0.32273376, 0.71003315]
```

### 출력층 설계
#### 소프트맥스
- overflow 문제
```python
a = np.array([1010, 1000, 990])
np.exp(a) / np.sum(np.exp(a))
>>> __main__:1: RuntimeWarning: overflow encountered in exp
>>> __main__:1: RuntimeWarning: invalid value encountered in true_divide
>>> array([nan, nan, nan])
np.exp(a - np.max(a)) / np.sum(np.exp(a - np.max(a)))
>>> array([9.99954600e-01, 4.53978686e-05, 2.06106005e-09])

def softmax(a):
    c = np.max(a)
    exp_a = np.exp(c - a) # 오버플로 대책
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y
```
- Since exponential function is monotone incresing, the order of each element of a does not change.
