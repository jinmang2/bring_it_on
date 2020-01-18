# Chapter 2. Perceptron
- 프랑크 로젠블라트(Frank Rosenblatt)가 1957년에 고안한 알고리즘

### What is perceptron?
- 다수의 신호를 입력으로 받아 하나의 신호를 출력
- 입력 신호가 뉴런에 보내질 때 각각 고유한 가중치가 곱해짐
- y = 1 if w1x1+w2x2+b > 0 else 0
- 가중치는 전류에서 말하는 **저항**에 해당.
    - 저항은 전류의 흐름을 억제하는 매개변수, 저항이 낮을수록 큰 전류가 흐름
    - 한편 퍼셉트론의 가중치는 그 값이 클수록 강한 신호를 흘려보냄

### Implement perceptron
```python
import numpy as np

class SingleGate:

    def __init__(self, gatename='AND'):
        if gatename.upper() == 'AND':
            W, b = (0.5, 0.5), -0.7
        elif gatename.upper() == 'NAND':
            W, b = (-0.5, -0.5), 0.7
        elif gatename.upper() == 'OR':
            W, b = (-0.2, -0.2), 0.1
        else:
            raise NotImplementedError(
            "Only have to input 'AND', 'NAND', 'OR' as gatename keyword argument.")
        self.W = np.array(W)
        self.b = np.array(b)
        
    def _getSignal(self, X):
        return np.sum(X * self.W) + self.b
        
    def _step(self, X):
        signal = self._getSignal(X)
        return 1 if signal > 0 else 0
        
    def run(self, X=None, mode='input'):
        Err_msg = "Change the mode to a 'truth_table' or type X input."
        Err_msg2 = "'mode' argument should only use one of 'input' and 'truth_table'."
        assert ~((mode == 'input') and (X is None)), Err_msg
        if mode is not 'input':
            if mode.lower() == 'truth_table':
                return {
                    (0, 0): self._step([0, 0]),
                    (0, 1): self._step([0, 1]),
                    (1, 0): self._step([1, 0]),
                    (1, 1): self._step([1, 1]),
                }
            else:
                raise NameError(Err_msg2)
        else:
            X = np.array(X)
            return self._step(X)
            
NAND = SingleGate('NAND')
OR = SingleGate('OR')
AND = SingleGate('AND')

NAND.run(mode='truth_table')
>>> {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 0}

OR.run(mode='truth_table')
>>> {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 1}

AND.run(mode='truth_table')
>>> {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}
```

### XOR problem
- 다중 퍼셉트론으로 해결
```python
def XOR(x1, x2):
    NAND = SingleGate('NAND')
    OR   = SingleGate('OR')
    AND  = SingleGate('AND')
    return AND.run(
        [NAND.run([x1, x2]), 
         OR.run([x1, x2])]
    )
    
XOR(0, 0), XOR(0, 1), XOR(1, 0), XOR(1, 1)
>>> (0, 1, 1, 0)
```
- 의의: 단층 퍼셉트론으로는 표현하지 못한 것을 층을 하나 늘려 구현할 수 있다.

### NAND에서 컴퓨터까지
- 다층 퍼셉트론은 지금까지 보아온 회로보다 복잡한 회로를 만드는 것이 가능
- 덧셈을 처리하는 가산기
- 2진수를 10진수로 변환하는 인코더
- 어떤 조건을 충족하면 1을 출력하는 회로(패리티 검사 회로)
- 컴퓨터 내부에서 이뤄지는 처리가 매우 복잡할 거 같지만 사실은 NAND 게이트의 조합만으로 컴퓨터가 수행하는 일을 재현하는 것이 가능
- The Elements of Computing Systems: Building a Modern Computer from First Principles, The MIT Press, 2005
- 2층 퍼셉트론 구조에서 가중치를 적절히 설정하여 컴퓨터를 만들기란 매우 힘듬
- 실제로도 NAND 등의 저수준 소자에서 시작하여 컴퓨터를 만드는 데 필요한 부품(모듈)을 단계적으로 만들어가는 쪽이 자연스러운 방법

#### 정리하면?
- 처음에는 AND와 OR 게이트
- 그다음에는 반가산기와 전가산기
- 그다음에는 산술 논리 연산 장치(ALU)
- 그다음에는 CPU

#### 중요한 것은?
- 퍼셉트론은 층을 거듭 쌓으면 비선형적인 표현도 가능하고, 이론상 컴퓨터가 수행하는 처리도 모두 표현할 수 있다는 
