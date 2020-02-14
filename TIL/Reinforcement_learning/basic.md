# 강화학습 기초
- 출처: 마키나락스 김기현님의 저서 [김기현의 자연어 처리 딥러닝 캠프-파이토치편]

## Definitions
```
Reinforcement Learning: 
    어떠한 객체가 주어진 환경에서, 상황에 따라 어떻게 행동해야 할지 학습하는 방법에 대한 학문
state: 
    상태
environment: 
    환경
agent: 
    객체
reward: 
    행동에 따른 보상
episode: 
    `상태-행동-보상`이 순차적으로 반복되는 시퀀스 (특정 조건이 만족되면 종료되는 유한 시퀀스)
```

## Markov Decision Process(MDP)
```
Define T=t: state.
Given t>0, The future(T>t) is independent from the past(T<t).
Then, Probability of changing from the current situation to the future is

    P(S'|S)
    
In MDP, Probability of changing to a future situation when you choose an action in the current situation is
    
    P(S'|S, A) 
```

## Reward
```
For each reward R_i(i in [t+1, t+2, ..., T],
Let G_t is cumulative sum of rewards.
In other words,

    G_t = R_{t+1} + R_{t+2} + R_{t+3} + ... + R_T

Let γ is discount factor such that γ in [0, 1].
By applying γ to G_t, rewrite formula G_t as follow;

    G_t = R_{t+1} + γ * R_{t+2} + γ^2 * R_{t+2} + ... = sum_{k=0}^{∞}{γ^k * R_{t+k+1}}

Note that: By discount rate γ, we can place more emphasis on rewards in the near future than in the far future.
```

## Policy
```
Note that: Given state, agent maximize cumulative sum of rewards.
Since maximize G_t, agent must have a criterion of how and under what circumstances.
Thus, define policy as follow;

Def policy, π
    Probabilistic criterion of how the agent should act according to the situation
    
    π(a|s) = P(A_t=a|S_t=s)
    
```

## Value Function / Action Value Function
```
Def value function
    Expected value of cumulative sum of total rewards from a given state s under a given policy π
    
    v_π(s) = E_π[G_t|S_t=s] = E_π[sum_{k=0}^{∞}{γ^k * R_{t+k+1}}|S_t=s], for all s in S.
    
Def action-value function(Q-function)
    Expected value of cumulative sum of total rewards for choosing action a in state s under a given policy π

    q_π(s) = E_π[G_t|S_t=s, A_t=a] = E_π[sum_{k=0}^{∞}{γ^k * R_{t+k+1}}|S_t=s, A_t=a]
```

## Bellman Equation
```
Note that: 
    - If function can be expressed by Bellman eq., 
      This means that you can approach problems with dynamic programming algorithms.
    - That is, just like finding the shortest path.

By Bellman equation, formula of action-value function can be rewritten as follow:
        
    v_*(s) = max_a{ E[ R_{t+1} + γ * v_*(S_{t+1}) | S_t=s, A_t=a ] }
           = max_a{ sum_{s', r}{ P(s', r | s, a)[r + γ * v_*(s')] } }
           
    q_*(s, a) = E[ R_{t+1} + γ * max_a'{ q_*(S_{t+1}, a') } | S_t=s, A_t=a ]
              = sum_{s', r}{ P(s', r | s, a)[r + γ * max_a{ q_*(s', a')] } }
```

## Monte Carlo method
```
Note that: 
    - P(s', r | s, a) is posterior probabilities.
    - Dynamic programming cannot be applied.
    - That is, the agent is trained through experiences such as simulation like reinforcement learning.
    
    V(S_t) ← V(S_t) + α[G - V(S_t)]
```
- 몬테카를로 방법처럼 샘플링을 통해 벨만 기대 방정식을 해결할 수 있음
- 문제는 긴 에피소드에 대해 샘플링으로 학습하는 경우
- 긴 에피소드일 경우 학습에 매우 많은 시간과 자원이 소모

## Temporal Difference Learning(시간차 학습)
- 에피소드 보상의 누적 합 없이도 바로 가치 함수를 업데이트할 수 있음
```
    V(S_t) ← V(S_t) + α[R_{t+1} + γV(S_{t+1}) - V(S_t)]
```

> ### Q-Learning
- 행동 가치 함수를 잘 학습하는 것
- 타깃과 현재 가치 함수 사이의 차이를 줄이면 결국 올바른 큐 함수를 학습하게 될 것.
```
    Q(S_t, A_t) ← Q(S_t, A_t) + α[R_{t+1} + γ*max_a{Q(S_{t+1}, a)} - Q(S_t, A_t)]
                                  ________________________________   ___________
                                          *--- target ---*          *- current -*
```

> ### Deep Q-Learning
- 큐 함수를 배울 때 상태 공간의 크기와 행동 공간의 크기가 너무 커서 상황과 행동이 희소할 때 문제 발생
- 상황과 행동이 불연속적인 별개의 값이더라고, 규 함수를 근사하면 문제를 해결할 수 있음
```
    Q(S_t, A_t) ← Q(S_t, A_t) + α[R_{t+1} + γ*max_a{Q(S_{t+1}, a)} - Q(S_t, A_t)]
                 ____________
             **--approximated--**
```

# Policy based Reinforcement Learning

## policy gradient
- DQN: value based reinforcement learning
- policy gradient: policy based reinforcement learning
- Difference?
    - value based: 인공신경망을 통해 어떤 행동을 선택했을 때 얻을 수 있는 보상을 예측하도록 훈련
    - policy based: 인공신경망의 행동에 대한 보상을 역전파 알고리즘을 통해 전달하여 학습
    - Thus, value based는 행동의 선택이 확률적으로 나오지 않고 policy based는 행동을 선택할 때 확률적인 과정을 거침
```
def policy gradient

    π_θ(a|s) = P_θ(a|s) = P(a|s;θ)
    
Note that: 
    - π means policy.
    - θ is weights parameter. Given 's', returns the probability of which action 'a' to choose.
    
    J(θ) = E_{π_θ}[r] = v_θ(s_0)
         = sum_{s in S}{ d(s) * sum_{a in A}{ π_θ(s, a)R_{s, a} } }

For maximize rewards, use 'gradient ascent' as follow:
    
    θ_{t+1} = θ_t + γ∇_θ{J(θ)}  
    
    where d(s): Stationary distribution of the Markov chain, 
                which is the percentage of time spent in s along the entire path, 
                regardless of the starting point.
    
By Differential properties of log function, we can get a ∇_θ{J(θ)}.

    ∇_θ{π_θ(s, a)} = π_θ(s, a) * {∇_θ{π_θ(s, a)} / π_θ(s, a)}
                   = π_θ(s, a) * ∇_θ{log(π_θ(s, a))} ...(1)   (∵ (logf(x))' = f'(x)/f(x))
                   
    ∇_θ{J(θ)} = sum_{s in S}{ d(s) * sum_{a in A}{ ∇_θ{π_θ(s, a)} R_{s, a} } }
              = sum_{s in S}{ d(s) * sum_{a in A}{ π_θ(s, a) * ∇_θ{log(π_θ(s, a))} R_{s, a} } } (By (1).)
              = E_{π_θ}[ ∇_θ{ log( π_θ(a|s) ) } * r ]

By policy gradient theorem,

    ∇_θ{J(θ)} = E_{π_θ}[ ∇_θ{ log( π_θ(a|s) ) } * Q^{π_θ}(s, a) ] ...(2)
    
Note that: 
    - Formula (2) means that there is no need to differentiate for the Q function.
    - That is, any function can be used as a reward function, regardless of whether it can be differentiated.
    
By Monte-Carlo sampling,

    θ ← θ + γQ^{π_θ}(s_t,a_t)∇_θ{log(π_θ(a|s))}
    
    where log(π_θ(a|s)): Given s_t, probability where the selected behavior is a_t, 
                         sampled from the probability distribution over the policy parameters.
          ∇_θ{log(π_θ(a|s))}: Differential value of log(π_θ(a|s)) for θ.
          Q^{π_θ}(s_t,a_t): Expected cumulative reward until end of episode.
          γ: Discount factor.
```
## MLE vs policy gradient

