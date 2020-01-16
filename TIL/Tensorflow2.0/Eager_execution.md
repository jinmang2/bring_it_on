# Eager execution
- Tensorflow 2.0 즉시 실행 기능
- 그래프를 생성하지 않고 함수를 바로 실행하는 명령형 프로그래밍 환경
- 나중에 실행하기 위해 계산 가능한 그래프를 생성하는 대신, 계산값을 즉시 알려주는 연산
- 이는 model debugging을 더욱 쉽게 만들고 불필요한 상용구 코드(boilerplate code) 작성을 줄여줌
- Eager execution은 연구와 실험을 위한 유연한 기계학습 플랫폼으로 다음과 같은 기능을 제공
  - 직관적인 인터페이스 코드를 자연스럽게 구조화하고 파이썬의 데이터 구조를 활용. 작은 모델과 작은 데이터를 빠르게 반복
  - 손쉬운 디버깅-실행 중인 모델을 검토하거나 변경 사항을 테스트해보기 위해서 연산을 직접 호출. 에러 확인을 위해 표준 파이썬 디버깅 툴을 사용
  - 자연스런 흐름 제어-그래프 제어 흐름 대신에 파이썬 제어 흐름을 사용함으로써 동적인 모델 구조의 단순화

## 코드로!
- 텐서플로 2.0에서 즉시 실행은 기본으로 활성화되어 있음
```python
import tensorflow as tf

tf.executing_eagerly()
```
```
2020-01-16 15:14:06.652598: I tensorflow/stream_executor/platform/default/dso_lo
ader.cc:44] Successfully opened dynamic library cudart64_100.dll

True
```
- TensorFlow 연산을 바로 실행할 수 있고 결과를 즉시 확인할 수 있음
```python
x = [[2.]]
m = tf.matmul(x, x)
print('hello, {}'.format(m))
```
```
hello, [[4.]]
```
- 즉시 실행 활성화는 텐서플로 연산을 바로 평가, 그 결과를 파이썬에 알려주는 방식으로 동작
- `tf.Tensor` 객체는 계산 그래프에 있는 노드를 가르키는 간접 핸들(symbolic handle)대신에 구체적인 값을 참조
- 출력하거나 확인하는 것이 그래디언트(gradient)를 계산하는 흐름을 방해하지 않음
- TensorFlow 수학 연산은 파이썬 객체와 Numpy 배열을 `tf.Tensor`객체로 변환
- `tf.Tensor.numpy` 메서드는 객체 값을 NumPy `ndarray`로 반환
```python
a = tf.constant([[1, 2], [3, 4]])
print(a)

# 브로드캐스팅(Broadcasting) 지원
b = tf.add(a, 1)
print(b)

# 연산자 오버로딩 지원
print(a * b)

# NumPy값 사용
import numpy as np

c = np.multiply(a, b)
print(c)

# 텐서로부터 numpy 값 얻기
print(a.numpy())
```
```
tf.Tensor(
[[1 2]
 [3 4]], shape=(2, 2), dtype=int32)
tf.Tensor(
[[2 3]
 [4 5]], shape=(2, 2), dtype=int32)
tf.Tensor(
[[ 2  6]
 [12 20]], shape=(2, 2), dtype=int32)
```

### 동적인 제어 흐름
- 즉시 실행의 가장 큰 이점은 모델을 실행하는 동안에도 호스트 언어의 모든 기능을 활용할 수 있음
- 아래와 같이 `fizzbuzz`를 손쉽게 작성할 수 있음
```python
def fizzbuzz(max_num):
    counter = tf.constant(0)
    max_num = tf.convert_to_tensor(max_num)
    for num in range(1, max_num.numpy()+1):
        num = tf.constant(num)
        if (int(num % 3) == 0) and (int(num % 5) == 0):
            print('FizzBuzz')
        elif int(num % 3) == 0:
            print('Fizz')
        elif int(num % 5) == 0:
            print('Buzz')
        else:
            print(num.numpy())
        counter += 1
```

### 즉시 훈련
#### 그래디언트 계산하기
- 즉시 실행을 사용하는 동안에, 나중에 그래디언트를 계산하는 연산을 추적하기 위해 `tf.GradientTape`을 사용하라
- 즉시 실행 중에 그래디언트를 계산하고 모델 훈련에 이용하기 위해서 `tf.GradientTape`을 이용할 수 있음.
- 특히 복잡하고 반복적인 훈련인 경우 더 유용.
- 매번 실행될 때 서로 다른 연산이 수행될 수 있기 때문에 모든 정방향(forward-pass) 연산은 'tape'에 기록.
- 그 다음 tape를 거꾸로 돌려 그래디언트를 계산한 후 tape를 폐기
- 특정한 `tf.GradientTape`는 오직 하나의 그래디언트만을 계산할 수 있고 부가적인 호출은 실행 중 에러(runtime error)를 발생
```python
w = tf.Variable([[1.0]])
with tf.GradientTape() as tape:
    loss = w * w

grad = tape.gradient(loss, w)
print(grad)
```
```
tf.Tensor([[2.]], shape=(1, 1), dtype=float32)
```

#### 모델 훈련
```python
# mnist 데이터 가져오기 및 포맷 맞추기
(mnist_images, mnist_labels), _ = tf.keras.datasets.mnist.load_data()

dataset = tf.data.Dataset.from_tensor_slices(
    (tf.cast(mnist_images[...,tf.newaxis]/255, tf.float32),
     tf.cast(mnist_labels,tf.int64)))
dataset = dataset.shuffle(1000).batch(32)

# 모델 생성
mnist_model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16,[3,3], activation='relu',
                           input_shape=(None, None, 1)),
    tf.keras.layers.Conv2D(16,[3,3], activation='relu'),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(10)
])

for images,labels in dataset.take(1):
    print("로짓: ", mnist_model(images[0:1]).numpy())
  
optimizer = tf.keras.optimizers.Adam()
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

loss_history = []

def train_step(images, labels):
    with tf.GradientTape() as tape:
        logits = mnist_model(images, training=True)
    
        # 결과의 형태를 확인하기 위해서 단언문 추가
        tf.debugging.assert_equal(logits.shape, (32, 10))

        loss_value = loss_object(labels, logits)

    loss_history.append(loss_value.numpy().mean())
    grads = tape.gradient(loss_value, mnist_model.trainable_variables)
    optimizer.apply_gradients(zip(grads, mnist_model.trainable_variables))
    
def train():
    for epoch in range(3):
        for (batch, (images, labels)) in enumerate(dataset):
            train_step(images, labels)
        print ('에포크 {} 종료'.format(epoch))
        
train()
```
```
Downloading data from https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz
11493376/11490434 [==============================] - 0s 0us/step
로짓:  [[-0.02961861 -0.03135324  0.01644302  0.01767892 -0.02153635  0.02689432
   0.02077326  0.02821362  0.01535387 -0.00981388]]
에포크 0 종료
에포크 1 종료
에포크 2 종료
```
