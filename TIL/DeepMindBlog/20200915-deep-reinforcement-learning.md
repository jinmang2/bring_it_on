# [Deep Reinforcement Learning](https://deepmind.com/blog/article/deep-reinforcement-learning)
`2020.09.15`

- DeepMind의 목적은 최상의 장기보상을 효과적으로 얻을 인간 수준의 agent를 구축하는 것
- 저레벨 모터 제어부터 고레벨 인지 태스크까지 인간과 동일한 성능을 내는  agent
- Agent는 좋은 행동을 취하는 가치 판단을 함
- 우리는 14년도에 DQN이라는 Q-network를 dl로 표현하는 알고리즘을 소개함
- 기존 RL+DL은 학습 불안정성(unstable learning) 때문에 학습에 실패했었음
- 그러나 DQN은 agent의 모든 경험을 저장하고 이를 임의로 샘플링하여 학습 데이터와의 자가상관성을 줄이고 다양성을 제공할 수 있는 경험을 재현함
- 실제로 atari에서 실험 시 50가지 게임 중 절반가량에서 human performance 달성
- 그 후 DeepMind는 아래 기법들을 활용, DQN의 성능을 높이려 시도, 현재 대부분의 atari 게임에서 human-p를 달성.
further stabilising the learning dynamics; prioritising the replayed experiences; normalising, aggregating and re-scaling the outputs.
- Golia로 알려진 분산 deep rl 시스템으로 학습 속도도 향상시킴
- DQN엔 아직도 문제 존재
- 때문에 16년도, asyncronous rl을 소개(비동기적)
- 이는 cpu 멀티스레딩 병렬화 처리를 가능하게 만들어줬고 DQN의 장점을 그대로 상속
- 이름하야 A3C. 액션을 선택할 때 deep policy network 사용.
- 2d atari를 정복했으니 3d labyrinch 제시(이 포스팅은 16년도)! A3C는 여기서도 HP달성
- episodic memory에 기반한 접근은 성공적
- 우리는 deep rl을 robotics manipulation, locomotion과 같은 연속 제어 문제에 적용할 계획 (Deterministic Policy Network)
- Go게임(체스를 의미하는 듯)은 수십년의 노력에도 이전 방법들은 아마추어 수준에 머물렀음.
- 우린 혼자 게임을 할 수 있게 승자를 예측하는 value network, 행동을 선택할 policy network 둘 다 학습하는 deep rl을 개발
- AlphaGo알제?
- atari에서 labyrinth, locomotion에서 manipulation, poker에서 go에 이르기까지 우린 짱이었음 :)
- 우린 이제 이 agent로 헬스케어와 같은 api를 활용하여 사회에 긍정적인 영향을 줄 것임
