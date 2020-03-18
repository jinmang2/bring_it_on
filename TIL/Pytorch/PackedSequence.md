# Pytorch PackedSequence Tutorial

## Trouble in ELMo Source Code... (biLSTM)
- AllenAI의 `ELMo`를 구현 중에 아래와 같은 코드를 만났다.
- biLSTM의 input으로 넣어주기위해 char-CNN에서 넘어온 input을 바꿔줘야하는데
- 아래와 같은 소스코드가 있어 분석하고자 한다.
- 이는 `Seq2xxxEncoder` class의 base class에서 `sort_and_run_forward` 메서드에서 확인할 수 있다.
```python
from torch.nn.utils.rnn import pack_padded_sequence, PackedSequence

sorted_inputs
>>> tensor([[[-0.0183, -0.0138, -0.0024,  ..., -0.0184, -0.0119,  0.0053],
>>>          [-0.0240, -0.0288, -0.0135,  ..., -0.0017, -0.0249,  0.0315],
>>>          [-0.0395, -0.0228,  0.0279,  ..., -0.0059, -0.0102,  0.0300],
>>>          ...,
>>>          [-0.0184, -0.0303, -0.0026,  ..., -0.0013,  0.0139, -0.0141],
>>>          [-0.0143, -0.0274,  0.0087,  ..., -0.0230, -0.0142,  0.0145],
>>>          [-0.0121, -0.0208, -0.0112,  ..., -0.0085, -0.0021, -0.0223]],
>>> 
>>>         [[-0.0183, -0.0138, -0.0024,  ..., -0.0184, -0.0119,  0.0053],
>>>          [-0.0309, -0.0024, -0.0106,  ..., -0.0335, -0.0177, -0.0154],
>>>          [-0.0270, -0.0023, -0.0187,  ..., -0.0012, -0.0226,  0.0049],
>>>          ...,
>>>          [-0.0045,  0.0003, -0.0031,  ...,  0.0018,  0.0065,  0.0052],
>>>          [-0.0045,  0.0003, -0.0031,  ...,  0.0018,  0.0065,  0.0052],
>>>          [-0.0045,  0.0003, -0.0031,  ...,  0.0018,  0.0065,  0.0052]],
>>> 
>>>         [[-0.0183, -0.0138, -0.0024,  ..., -0.0184, -0.0119,  0.0053],
>>>          [-0.0329, -0.0185, -0.0054,  ...,  0.0058, -0.0454,  0.0163],
>>>          [-0.0234, -0.0538, -0.0093,  ..., -0.0023, -0.0256,  0.0496],
>>>          ...,
>>>          [-0.0045,  0.0003, -0.0031,  ...,  0.0018,  0.0065,  0.0052],
>>>          [-0.0045,  0.0003, -0.0031,  ...,  0.0018,  0.0065,  0.0052],
>>>          [-0.0045,  0.0003, -0.0031,  ...,  0.0018,  0.0065,  0.0052]]],
>>>        device='cuda:0', grad_fn=<IndexSelectBackward>)

sorted_index.shape
>>> torch.Size([3, 10, 512])

sorted_sequence_lengths
>>> tensor([10,  7,  6], device='cuda:0')

packed_sequence_input = pack_padded_sequence(sorted_inputs,
                                             sorted_sequence_lengths.data.tolist(),
                                             batch_first=True)
packed_sequence_input                                             
>>> PackedSequence(
>>>        data=tensor(
>>>            [[-0.0183, -0.0138, -0.0024,  ..., -0.0184, -0.0119,  0.0053],
>>>             [-0.0183, -0.0138, -0.0024,  ..., -0.0184, -0.0119,  0.0053],
>>>             [-0.0183, -0.0138, -0.0024,  ..., -0.0184, -0.0119,  0.0053],
>>>             ...,
>>>             [-0.0184, -0.0303, -0.0026,  ..., -0.0013,  0.0139, -0.0141],
>>>             [-0.0143, -0.0274,  0.0087,  ..., -0.0230, -0.0142,  0.0145],
>>>             [-0.0121, -0.0208, -0.0112,  ..., -0.0085, -0.0021, -0.0223]],
>>>            device='cuda:0', 
>>>            grad_fn=<PackPaddedSequenceBackward>), 
>>>        batch_sizes=tensor([3, 3, 3, 3, 3, 3, 2, 1, 1, 1]), 
>>>        sorted_indices=None, 
>>>        unsorted_indices=None)

packed_sequence_input.data.shape
>>> torch.Size([23, 512])
```
- 우선 위의 코드로 어떤 역할을 수행하는 것인지 생각해보자.
- input vector의 크기는 `(3, 10, 512)`이다.
- 3은 batch_size를 의미하며 10은 각 문장의 최대 길이(bos, eos를 포함한), 그리고 512는 char-CNN을 거쳐서 생성된 2,048D를 축소한 차원이다.
- 처음 input text는 아래와 같았다.
  ```python
  # Example Inputs
  sents = [['발', '없는', '말이', '천리', '간다'],
           ['다시', '사랑한다', '말', '할까'],
           ['유독', '너와', '헤어지다', '싫다', '밤', '집', '으로', '돌아가다']]
  ```
- 총 3개의 문장(batch_size)로 되어있는 `sents`의 각 문장별 길이를 계산하면 아래와 같이 산출된다.
  ```python
  # Since <BOS> and <EOS>, len(sent) += 2
  # BOS: Begin of Sentence
  # EOS: End of Sentence
  
  [len(sent) + 2 for sent in sents)
  >>> [7, 6, 10]
  ```
- 위의 코드에서 `sorted_sequence_lengths`가 위의 `list`를 정렬하게 `torch.Tensor`로 바꾼 객체이다.
- 위 객체에 `sorted_sequence_lengths.data.tolist()` 메서드를 실시하게 되면 `list` 객체를 반환한다.
- `sorted_inputs`, `sorted_sequence_lengths.data.tolist()` 두 개의 input을 `pack_padded_sequence`함수의 argument로 넣어 실행을 시켜주면
- `(23, 512)`차원의 vector와 `batch_size=[3,3,3,3,3,3,2,1,1,1]`의 총합 23인 batch_size를 인자로 가지는 `PackedSequence`객체를 반환하게 된다.
- `sorted_sequence_lengths`를 생각해보라. `sum([7, 6, 10])`은 `23`이지 않는가?
- 잘 생각해보면, 처음 `(3, 10, 512)`차원으로 계산하게 되면 `(30, 512)`차원으로 ravel시켜 학습을 진행하게 될 것이다.
- 그러나 실제로 사용하는 문자는 10+6+7=23개 뿐이다! 나머지 7개는 `pad_char`이다!
- 즉, batch별 현재는 23%나 무의미한 연산을 실시한다는 것을 의미하며 이는 길이가 긴 문장과 짧은 문장이 고루 존재할 때 더 심각한 `sparsity`를 야기할 것이다.
- 이에 대한 해결 방법은?
  - RNN의 히든 스테이트가 이전 타임스탭에 의존해서 최대한 많은 토큰을 병렬적으로 처리
  - 각 문장의 마지막 토큰이 마지막 타임스텝에서 계산을 멈춰야한다.
  - `위 두 문장은 https://simonjisu.github.io/nlp/2018/07/05/packedsequence.html의 내용을 그대로 복붙하였음을 알립니다.`
- 나의 예제로 한번 어떻게 동작하는지 살펴보자!!

## Pytorch API
- 사실 처음에는 `torch`에서 구현되있는 코드를 하나하나 따라가보며 실습하려고 했었다.

```python
# torch.nn.utils.rnn.py

from collections import namedtuple
import warnings
import types
import sys

import torch

# from .. import _VF
class VFModule(types.ModuleType):
    def __init__(self, name):
        super(VFModule, self).__init__(name)
        self.vf = torch._C._VariableFunctions

    def __getattr__(self, attr):
        return getattr(self.vf, attr)

_VF = VFModule(__name__)

# from ..._jit_internal import Optional
try:
    from typing import Optional
except:
    class DictInstance(object):
        __slots__ = ['__args__']

        def __init__(self, types):
            self.__args__ = types

    class DictCls(object):
        def __getitem__(self, types):
            return DictInstance(types)

    Optional = DictCls()  # noqa: T484

PackedSequence_ = namedtuple('PackedSequence',
                             ['data', 'batch_sizes', 'sorted_indices', 'unsorted_indices'])

# type annotation for PackedSequence_ to make it compatible with TorchScript
PackedSequence_.__annotations__ = {'data': torch.Tensor, 'batch_sizes': torch.Tensor,
                                   'sorted_indices': Optional[torch.Tensor],
                                   'unsorted_indices': Optional[torch.Tensor]}
                                   
...
def pack_padded_sequence(input, lengths, batch_first=False, enforce_sorted=True):
    """Packs a Tensor containing padded sequences of variable length."""
    lengths = torch.as_tensor(lengths, dtype=torch.int64)
    if enforce_sorted:
        sorted_indices = None
    else:
        lengths, sorted_indices = torch.sort(lengths, descensing=True)
        sorted_indices = sorted_indices.to(input.device)
        batch_dim = 0 if batch_first else 1
        input = input.index_select(batch_dim, sorted_indices)
    
    data, batch_sizes = \
        _VF._pack_padded_sequence(input, lengths, batch_first)
    return PackedSequence(data, batch_sizes, sorted_indices, None)
...
```
- Python은 C로 작성됬다. Pytorch의 imperative engine도 C로 작성되있다.
- C의 library를 부르는 pyfile확장자는 `.pyd`이다.
- 이 얘기를 왜 꺼내냐면,
    - `pack_padded_sequence` 함수를 호출하면 마지막에 `_VF._pack_padded_sequence`로 data와 batch_size를 계산한다.
    - `_VF`는 `_VF = VFModule(__name__)`으로 정의된다.
    - `VFModule`은 `__getattr__` 매직 명령어가 호출되면 `self.vf`의 메서드를 호출한다.
    - `self.vf`는 `torch._C._VariableFunctions`이다.
- 자, 근데 여기서 문제!
    - `torch._C`는 `~/site-packages/torch/_C.cp36-win_amd64.pyd`에 작성되있다.
    - 아니 근데 이 파일을 읽을 수가 없어...
    - 설사 읽는다고 한들 C언어 라이브러리를 python에서 사용하는 것이기 때문에 너무 딥하게 들어갈 여지가 크다.
- 때문에, 이미 누군가가 정리한 `torch`의 실습 예제를 참고, 어떤 식으로 동작하는지 공부하고자 한다.

## Pytorch - PackedSequence




출처: 
- https://simonjisu.github.io/nlp/2018/07/05/packedsequence.html
- https://medium.com/huggingface/understanding-emotions-from-keras-to-pytorch-3ccb61d5a983
