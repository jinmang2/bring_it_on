# Multi-task and Meta learning

첼시 핀 교수님께서 자신의 연구 분야를 설명하며 아래 질문을 던지셨다.
- `How can we enable agents to learn skills in the real world?`

자신의 석사 연구생활을 언급하시며 로봇 팔 움직임에 대한 연구를 소개하며 아래 이슈를 공유
- `The robot didn't learn how to use spatulas to lift objects into bowls`

상세한 supervision 혹은 guidance가 없으면 single task를 학습 시 bowl 색이 바뀌거나 주변 환경의 조그마한 변화에도 로봇은 엉망이 되버림

아기나 너희가 학습하는 방식을 생각해봐라.

## Why Deep?
DL은 unstructured input 처리를 가능케 함.

Large, Diverse data (+ Large Model) -> Broad generalization!

## Then, why multi-task and meta-learning?
아래 질문들을 생각하라.

```
What if you want a more general-purpose AI System?
What if you don't have a large dataset?
What if your data has a long tail?
What if you need to quickly learn structure now? -> 최초엔 few-shot
```

## What is task?
Given Dataset D and Loss L, generate function f_theta.

각 task들은 dataset과 loss의 분포가 다양함!!

## Critical Assumption
- Bad News: Different tasks need to share some structure
- Good News: There are many tasks with shared structure

Meta-learning; 기반 태스크 구조를 배우는 모든 종류를 통칭

## Multi-task vs Meta ([학생의 질문](https://youtu.be/0rZtSwNOTQo?t=2138), [rough definition](https://youtu.be/0rZtSwNOTQo?t=2181))
- **The multi-task learning problem**: Learn all of the tasks more quickly or more proficiently than learning them independently
  - 주어진 모든 task 문제를 빠르고 능숙하게 독립적으로 처리하는 것 (아래 질문글 보면, 굉장히 러프한 정의가 맞음.)
- **The meta-learning problem**: Given data/experience on previous tasks, learn a new task more quickly and/or more proficiently
  - 이전에 배운 학습을 기반으로 다음 task 문제를 더 빠르고 능숙하게 처리
  
## Meta-learning vs Transfer learning?? ([Question](https://youtu.be/0rZtSwNOTQo?t=2275))

```
A form of transfer learning problem statement where you wanna take some data and 
use knowledge acquired from that data to do well at other tasks 
I think that one aspect about this problem statement is that you want to be able to learn a new task more quickly, 
whereas in transfer learning you may also want to be able to just form a 
well-performing a new task well in zero shot where you kind of just want to share representations.
I actualy kind of view transfer learning as something that encapsulates both of these things, 
uh where you're thinking about how you can transfer information between different tasks and 
that could actually also correspond to the multitask learning problem as well as the meta learning problem.
```
**정확한 번역이 아님을 주의**
- transfer learning에서의 두 problem statement `well-perform`, `quickly`
- 

#### [Differences between Transfer Learning and Meta Learning](https://stackoverflow.com/questions/60261727/differences-between-transfer-learning-and-meta-learning)
In [Quora](https://www.quora.com/In-machine-learning-what-is-the-difference-between-the-terms-transfer-learning-multitask-learning-inductive-transfer-meta-learning-and-learning-to-learn/answer/Mustafa-Orkun-Acar),
> Meta learning은 ML process를 개선하기 위해 어떤 case에 대한 meta-data에 일부 알고리즘을 적용하는 ML Theorey의 일부
> Meta-data는 사용된 알고리즘에 대한 속성, 학습 작업 자체 등이 포함됨
> Meta-data를 사용하면 문제를 더 효율적으로 풀기 위한 학습 알고리즘을 더 잘 고를 수 있다.

In [TowardDataScience](https://towardsdatascience.com/icml-2018-advances-in-transfer-multitask-and-semi-supervised-learning-2a15ef7208ec),
> 전이 학습은 다소 유사한 선행 문제를 해결하여 얻은 **경험**을 사용하여 새로운 작업을 학습하는 과정을 개선하는 것이 목표
> 실용적으론 대부분 ML model들은 단일 task를 처리하기 위해 디자인됨.
> 하지만 사람은 미래에 같은 작업을 반복하거나 새로운 작업을 배울 때 과거의 경험을 사용
> 즉, 만약 우리가 풀고자 하는 문제가 과거에 푼 것과 비슷하다면, 이는 우리에게 쉬울 것임
> 그러므로 ML에서 같은 학습 접근법을 사용하기 위해 전이 학습은 하나 이상의 소스 작업의 과거 경험을 전달하고 (multi-task) 이를 사용하여 관련 대상 적업에서 학습을 향상시키는 방법을 포함

![img](https://miro.medium.com/max/700/1*9bXvgvgVQg8Zq6eKSa0rCw.png)

근데 위 두 article을 읽어도 질문자는 아직 `meta-learning`, `transfer-learning`, `meta-transfer learning`에 대한 용어들이 헷갈린다고 질문함.

이에 대해 답변자([Kaiyuan Xu](https://stackoverflow.com/users/12087535/kaiyuan-xu))가 언급하길,
```
각 tasks들이 유사한지 아닌지!
전이 학습에서는 각 모수들은 다음 task로 바로 전달되지만
메타 학습에서는 이전 task를 어떻게 풀었느냐가 아니라 어떻게 배웠는지를 부호화하여 모수를 넘겨야 하기 때문에
모수가 선택적으로 전이된다고 함.
```

이에 대해 질문자는 아래와 같이 comment를 남김
- 답변 고마워! (Survey of Transfer Learning)[https://www.cse.ust.hk/~qyang/Docs/2009/tkde_transfer_learning.pdf]의 page 5에 따르면,
- `multi-task learning`은 `transfer-learning`의 하위 항목이래!
- 이 tasks들은 각각 유사할 필요는 없지만 어느 정도 공통점은 공유한다네! (같은 것 아닌가...)
- 나 이거 보면서 추가로 공부했어! [Difference between multitask learning and transfer learning - StackExchange](https://stats.stackexchange.com/questions/255025/difference-between-multitask-learning-and-transfer-learning)

위 글 보니, multi-task learning은 1997년부터 이어져온 개념같음. 이때 이미 learning to learn이란 키워드 존재.



- **Transfer Learning**
  - **Finetuning:** This is probably the pardigm of transfer learning that you are most familiar with. Here we have both source and target distributions, S(y|x) and T(y2|x2), where x  ≠ x2 and y1  ≠ y2. To fine tune you must have some labeled data in the target domain. We transfer knowledge by freezing the upper and intermediate layers, using a decaying LR etc. and adding lower layers trained specifically for the new classes. 
  - **Multitask Learning**: Here we have multiple tasks T1, T2, T3...Tn; these tasks are trained jointly. An example is you might train a multitask network for both sentiment classification and named entity recognition simultaneously. This is a form of TL because essentially you are transfering knowledge between the two during training.
  - **Domain Adaptation**: This is similar to fine-tuning except ONLY the domain changes not the set of labels. So given two distributions S(y|x), T(y|x2) x ≠ x2, but y is the same. Most domain adaptation focuses on the unsupervised case where there is no labeled data in the target domain. Example: Adapting a model of labeled photos of cars from a simulator (source domain) to  unlabeled cars on streets (target domain). 

- **Metalearning (life-long learning):**  The goal of Meta-learning is to learn "general" properties (hyperparameters or weights) that are highly adaptable to new tasks. It learns these based on being trained on a large number of different tasks. In a way meta-learning can almost be thought of as "historical" multi-task learning in that it uses multiple different tasks to find this ideal set of properties. Recently, meta-learning tends focus on finding "model agnostic" solutions where as multi-task learning remains deeply tied to model architecture.



