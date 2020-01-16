# `@.tf.function`
## Stackoverflow

`@tf.function` converts to Python function to its graph representation
Usually, the code look like;
```python
# model,loss, and optimizer defined previously

@tf.function
def train_step(features, labels):
   with tf.GradientTape() as tape:
        predictions = model(features)
        loss_value = loss(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss_value

for features, labels in dataset:
    lv = train_step(features, label)
    print("loss: ", lv)
```

## Tensorflow Docs
### Better performance with `tf.function` and `AutoGraph`
- Tensorflow 2.0은 간단한 실행과 tf 1.0의 이점을 모두 챙김
- `tf.function` 데코레이터를 사용하면, 기존과 같이 함수를 부를 수 있을 뿐만 아니라 graph로 compile하기 때문에 GPU, TPU로 돌릴 때 속도면에서 빠른 이점을 얻을 수 있다.
```python
@tf.function
def simple_nn_layer(x, y):
    return tf.nn.relu(tf.matmul(x, y))

x = tf.random.uniform((3, 3))
y = tf.random.uniform((3, 3))

simple_nn_layer(x, y)
```
```
<tf.Tensor: shape=(3, 3), dtype=float32, numpy=
array([[0.765691  , 0.836447  , 0.71503663],
       [0.6713706 , 0.64472127, 0.6218941 ],
       [0.22329617, 0.47106054, 0.09977148]], dtype=float32)>
```
주석의 결과를 살펴보면 TensorFlow 런타임과의 모든 상호 작용을 처리하는 특수 호출 가능임을 알 수 있다.
```
simple_nn_layer
```
```
<tensorflow.python.eager.def_function.Function at 0x7fe4f84f8e80>
```
multiple function을 사용할 때, 모든 함수에 decorator를 달 필요는 없다. 아래와 같이 작성하면 해당 코드는 graph mode에서 돌아갈 것이다.
```python
def linear_layer(x):
    return 2 * x + 1
    
@tf.function
def deep_net(x):
    return tf.nn.relu(linear_layer(x))
    
deep_net(tf.constant((1, 2, 3))
```
```
<tf.Tensor: shape=(3,), dtype=int32, numpy=array([3, 5, 7], dtype=int32)>
```



출처
- https://stackoverflow.com/questions/55149026/tensorflow-2-0-do-you-need-a-tf-function-decorator-on-top-of-each-function
- https://www.tensorflow.org/guide/function
