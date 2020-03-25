# Leaky integrator
Leaky integrator: 특정한 미분 방정식

입력의 적분을 취하지만 시간이 지남에 따라 점차 소량의 입력을 누설하는 요소나 시스템을 설명하는 데 사용

주로 하나의 neuron 혹은 neuron의 local population을 표현해야하는 **hydraulics**, **electronics**, **neuroscience**에서 나타난다.

이는 interest 주파수보다 훨씬 낮은 차단 주파수를 가진 1st-order [lowpass filter](https://en.wikipedia.org/wiki/Low-pass_filter)와 같다고 하네요.

## Equation
$$\cfrac{dx}{dt}=-Ax+c$$ where C: input, A: rate of the leak

non-homogeneous first-order linear differential equation

## 참고
https://en.wikipedia.org/wiki/Leaky_integrator
