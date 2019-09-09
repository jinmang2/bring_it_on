# 출처 : https://github.com/makeduck/makeduck.github.io

1. 패턴인식
2. 기계학습

facebook
https://www.facebook.com/events/1437133903231340

이하 페북메시지 스크랩

A.통계기반 고전적 기계학습(혹은 패턴인식?)
B.probabilistic graphical model 기반
C.신경망 기반(이건 딥러닝때문에 다시 각광)
-----------------------
D.reinforcement learning
기계학습은 대략 저런 입장으로 크게 나뉘어서 책과 강의가 있습니다.
책으로 보자면
A)
1. duda의 "pattern classifictaion"을 패턴인식 계열에서 많이들 봐왔고
http://as.wiley.com/WileyCDA/WileyTitle/productCd-0471056693.html
2. The Elements of Statistical Learning: Data Mining, Inference, and Prediction
http://statweb.stanford.edu/~tibs/ElemStatLearn/
A의 1번책이 좀 더 실용적이고 패턴인식에 맞춰져 있다면 2번 책이 좀 더 기초,이론적인 책이라 이걸로 시작하거나 읽으시는 분들도 많습니다. 좀 더 수학적이죠. 근데 이걸 쓴 저자들이 R을 이용해서 좀 더 쉽고 예제 위주로 쓴 책이 나왔어요.
3. An Introduction to Statistical Learning, with Applications in R
A의 2번책의 더 쉽고 응용중심의 책이 이겁니다. 스탠포드에 이걸 기반으로 강좌도 하나 열었죠. http://online.stanford.edu/course/statistical-learning-winter-2014
A에 속한 책들은 좀 기법을 모아놓은 듯한 느낌이 있습니다. 기존의 기계학습이 '해당 여러 기법들 모음'이라는 식이었죠. 통합하는 이론이 없었으니까요. 그걸 좀 더 확률적 관점(특히 베이지안)을 강화해서 일관성있게 설명하려고 하는 시도들이 B의 책들입니다.
B)
1. bishop의 Pattern Recognition and Machine Learning 이 이 분야의 최고봉 책이죠. B번 접근을 이끌고 있는 사람입니다. PGM(확률그래프모델링)의 관점으로 기존의 기계학습쪽을 설명하고 있습니다. 이 책 나오기 전에 공부했느냐 후에 공부했느냐에 따라 기계학습 공부 세대를 나누기도 합니다.
http://www.amazon.com/Pattern-Recognition-Learning-Information-Statistics/dp/0387310738/ref=pd_sim_b_1?ie=UTF8&refRID=0K9D3X9XXGK0XNRCS2CA
2. murphy의 Machine Learning: A Probabilistic Perspective
B의 1번책을 좀 더 보강하고 쉽게 쓰고 더 넓게 다루겠다고 나온 책입니다. 이 분야의 거두죠 머피도. 베이지안 네트워크쪽으로 집중하던 사람이구요.
http://www.amazon.com/Machine-Learning-Probabilistic-Perspective-Computation/dp/0262018020
근데 B의 1,2번 책들은 좀 더 어렵고, A을 알고 보는게 좋을 수 있습니다. 다만 A에 익숙해지면 B식으로 사고하기가 어렵다고도 하고. 또 B에 소개한 책 저자들이 수학배경이 강하고 영국사람들이라서 용어라던가, 서술방식 등이 미국중심의 기계학습 책이랑(즉 한국에서 많이 공부하는 책, 논문들과) 다르다고 하는군요.
C)는 요새 딥러닝 진영이 각광받으면서 다시 뜨고 있는거구요, D)는 A,B,C에서 안다루는 접근법의 방식입니다. 전통적인 기계학습의 구분이 - supervised learning과 unsupervised learning, 그리고 reinforcement learning 이렇게 3가지로 되는데 보통 기계학습 책들은 앞의 2개만 중점적으로 다루죠. A,B,C 책들은 supervised learning과 unsupervised learning이 쪽만 설명하겠다고 말하며 시작합니다. reinforcement learning은 주로 로보틱스 등의 제어, 경영과학이나 심리학의 의사결정 파트에서 사용하기 시작한다고 들었습니다.
제가 아는 한의 기계학습 관련한 책들은 위의 것과 같습니다.


(입문)
A. 코세라에 있는 앤드류 응의 머신러닝 강좌
https://www.coursera.org/course/ml
봉성주님이 추천해준 강좌가 좋습니다. 솔
직히 A계열에 속하는 기계학습 입문은 코세라에 여러개 열리고, udacity에도 열려 있어서 뭘 들어도 좋습니다.
심지어 duda의 패턴인식 책은 한글로 번역도 되어 있고, 그 외에도 한글로 번역된 파이썬이나 R을 이용한 기계학습 관련 책들을 읽어도 다 좋습니다.
개념을 아시고 주요 수식만 보셔도 될듯요. 하지만 제가 들은 것에는 코세라의 응 교수 수업이 쉽고 재밌고, 좀 더 이론 중심으로 해줍니다.
그리고 앤드류 응이 딥러닝 권위자고 하니까 그가 가진 관점이 녹아있는 부분들이 좀 있어서 추천해드립니다. 참고로 전 끝까지 듣지는 못했습니다.

B. 코세라에 있는 PGM 강좌
https://www.coursera.org/course/pgm
B쪽 책들은 좀 어렵고, 강좌도 별로 없는데 코세라에 PGM 강좌가 있더군요. 이거 들어두시면 이후에 현대 기계학습의 주요 경향을 따라가기 수월할 거라 생각합니다.
그 뒤에 저 위의 책들을 시도해보시면 좋을듯하네요.
책으로는 전 A-3 3. An Introduction to Statistical Learning, with Applications in R을 추천합니다.
