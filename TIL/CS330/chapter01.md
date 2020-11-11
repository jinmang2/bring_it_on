# Introduction & Overview

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
이런 문제들을 해결하기 위해 multi-task 및 meta-learning으로 발전

## What is task?
Given Dataset D and Loss L, generate function f_theta.

각 task들은 dataset과 loss의 분포가 다양함!!

## Critical Assumption
- Bad News: Different tasks need to share some structure
- Good News: There are many tasks with shared structure

Meta-learning; Learning to Learn의 General Properties를 학습하는 것이 목표

## Multi-task vs Meta
- **The multi-task learning problem**: Learn all of the tasks more quickly or more proficiently than learning them independently
  - 주어진 모든 task 문제를 빠르고 능숙하게 독립적으로 처리하는 것 (아래 질문글 보면, 굉장히 러프한 정의가 맞음.)
  - 왜 independently??
- **The meta-learning problem**: Given data/experience on previous tasks, learn a new task more quickly and/or more proficiently
  - 이전에 배운 학습을 기반으로 다음 task 문제를 더 빠르고 능숙하게 처리
  
**본 강의에서 multi-task 및 meta learning에 대한 모든 알고리즘을 다루진 않음.**
  
### Question 1. Meta-learning vs Transfer learning?? ([Question](https://youtu.be/0rZtSwNOTQo?t=2275))

>Yeah, So i guess in many ways i think that this is 
>A form of transfer learning problem statement where you wanna take some data and 
>use knowledge acquired from that data to do well at other tasks.
>I think that one aspect about this problem statement is that you want to be able to learn a new task more quickly, 
>whereas in transfer learning you may also want to be able to just form a 
>well-performing a new task well in zero shot where you kind of just want to share representations.
>I actualy kind of view transfer learning as something that encapsulates both of these things, 
>uh where you're thinking about how you can transfer information between different tasks and 
>that could actually also correspond to the multitask learning problem as well as the meta learning problem.

- meta-learning은 transfer learning의 problem statement의 한 형태라고 생각
- 어떤 problem statement? 데이터를 가져와 그 데이터에서 얻은 지식을 사용하여 다른 작업을 잘 수행하는 것
- 위 문제 진술에서 새로운 작업을 더 빨리 배울 수 있기를 원할 수도 있고
- 또 Zero-Shot에서 새로운 작업을 잘 수행(well-performed)하기를 원할 수도 있음 (같은 표현을 공유하면서)
- 첼시 핀 교수님께서는 전이학습은 위 두 문제 진술의 측면을 encapsulate하는 것이라고 생각
- 어떻게하면 서로 다른 task간의 정보를 전달할 수 있을 것인가를 연구 주제로 생각
- 이는 meta-learning뿐만 아니라 multi-task learning에서도 생각할 수 있음.

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

### Question 2. There could be no meta-learning with one single task? ([Question](https://youtu.be/0rZtSwNOTQo?t=2334))
> Good Point!
> In principle, you could still perform meta learning in context of a single task and what you'll 
> be doing in that case is probably actually in some ways breaking down that single task into sub-tasks or
> into kind of sub-components, uh and then using that when kind of when you're facing something new in
> that single task, using that experience to more quickly learn in the future. umm, Yeah, so that's a good point.
> The tasks in some ways could be something thats's kind of latent to your underlying problem. Yeah.

### Question 3. Is Meat-Learning and Domain Adaptation same? ([Question](https://youtu.be/0rZtSwNOTQo?t=2395))
> Yeah, so i'll formally cover the distinction with domain adaptation in the next lecture,
> but, um, in some ways they are similar. I guess in some ways, uh
> one is more specific than the other and in some ways it's kind of the opposite.
> So in domain adaptation, you typicallydo want to it's kind of a form of transfer learning in
> some ways where you want to transfer from one to another.
> Um, one thing and i guess when i get into the more formal definitions of these problems,
> this will become more clear, one thing you typically see in the meta-learning problem is 
> that the tasks that you're seeing in test time you assume to be in the distribution of the tasks
> that you're seeing it during training, whereas many techniques in domain adaptation are considering
> a setting where your task domain may be out of distribution from what you're seeing during training
> so that's in many ways one of those distinctions there.


## Doesn't multi-task learning reduce to single-task learning?
D = Summation{D_i}, L = Summation{L-i} --> single task learning!!

Yes, It can!
- Aggregating the data across tasks & learning a single model is one approach to multi-task leanring 

But, we can often do better!
- Exploit the fact that we know that data is coming from different tasks

## Why now? Why should we study deep multi-task & meta-learning now?

- _Multitask Leraning_ Caruanam, 1997
- _Is Learning The n-th Thing Any Easier Than Learning The First?_ Thrun, 1998
- _On the Optimization of a Synaptic Learning Rule_ Bengio et al. 1992

learning to learn!!

이 알고리즘들은 ML Research에서 근본적인 역할을 계속해서 수행해옴

- _Multilingual machine translation_
- _One-shot imitation learning from humans_
- _Multi-domain learning for sim2real transfer_
- _YouTuve recommendations_

Increasing role!!
- paper citation이 계속 증가 ㅎㅎ
- _How transferable are features in a deep neural network?_ Yosinski et al., 15
- _Learning to learn by gradient descent by gradient descent_ Andrychowicz et al., 15
- _Model-agnostic meta-learning for fast adaptation of deep networks_ Finn et al., 17
- _An overview of multi-task learning in neural networks_ Ruder, 17

Deep Learning 연구의 democratization!


## But, we still have many open questions and challenges!
