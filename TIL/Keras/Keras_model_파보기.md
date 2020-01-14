# Keras 모델 파보기
- keras를 이용해서 NN을 설계할 때 주로 `Sequential`을 사용, 선형적으로 쭉 이어진다면 이렇게 설계해도 무방
- 그러나 글쓴이가 GAN을 간단하게 설계하고 쭉 봤을 때, 복잡한 모델들이 많이 존재했음. 이를테면
  - 이미 만든 모델에서 일정 부분만 가져와서 새로운 모델 만들기
  - 이미 만든 모델들을 합쳐서 새로운 모델 만들기
- 이를 원활하게 해주기 위해 `keras.models` class를 파악하는 것이 필요
- 이미 '학습한'모델을 재사용하고 싶을 때, 그럴때 model을 사용하는 것 같다고 함

## make NN by Sequential
- `Sequential` 복습
- `Sequential`의 특징은 input이 없음
```python
# 아래 코드는 직접 손수 옮기며 내가 배운 것을 한올 한올 기억

### data reading
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
X_train, y_train = mnist.train.images, mnist.train.labels
X_test, y_test = mnist.test.images, mnist.test.labels

from keras.models import Sequential, Model
from keras.layers import Input, Dense, Activation
from keras.optimizers import Adam, SGD
from keras import metrics

## sequential model
seq_model = Sequential([
  Dense(512, input_shape=(784, ), activation='relu'),
  Dense(128, activation='relu'),
  Dense(32, activation='relu'),
  Dense(10, activation='softmax'),
])

print('#### Sequential Model")
seq_model.summary()
seq_model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(lr=1e-3, beta_1=0.9, beta_2=0.999, epsilon=1e-8),
                  metrics=[metrics.categorical_accuracy])
train_history = seq_model.fit(X_train, y_train, epochs=5, batch_size=500, verbose=2)
train_history = train.history.history # epoch마다 변화한 loss, metric

loss_and_metric = seq_model.evaluate(X_train, y_train, batch_size=128, verbose=0)
print('train, loss and metric: {}'.format(loss_and_metric))
loss_and_metric = seq_model.evaluate(X_test, y_test, batch_size=128, verbose=0)
print('test, loss and metric: {}'.format(loss_and_metric))
```
- input layer가 없음
```
Extracting MNIST_data/train-images-idx3-ubyte.gz
Extracting MNIST_data/train-labels-idx1-ubyte.gz
Extracting MNIST_data/t10k-images-idx3-ubyte.gz
Extracting MNIST_data/t10k-labels-idx1-ubyte.gz
#### Sequential Model
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
dense_74 (Dense)             (None, 512)               401920    
_________________________________________________________________
dense_75 (Dense)             (None, 128)               65664     
_________________________________________________________________
dense_76 (Dense)             (None, 32)                4128      
_________________________________________________________________
dense_77 (Dense)             (None, 10)                330       
=================================================================
Total params: 472,042
Trainable params: 472,042
Non-trainable params: 0
_________________________________________________________________
Epoch 1/5
5s - loss: 0.4589 - categorical_accuracy: 0.8673
Epoch 2/5
4s - loss: 0.1492 - categorical_accuracy: 0.9570
Epoch 3/5
5s - loss: 0.0983 - categorical_accuracy: 0.9716
Epoch 4/5
5s - loss: 0.0712 - categorical_accuracy: 0.9784
Epoch 5/5
5s - loss: 0.0515 - categorical_accuracy: 0.9844
train, loss and metric: [0.041054270681467921, 0.98849090910824866]
test, loss and metric: [0.078584650909528139, 0.97660000000000002]
```
## make NN by Model
- `keras.Model`을 사용하여 뉴럴넷을 설계
- 이전, kaggle 문제를 CNN으로 풀 때 한번 사용해봄.
```python
inputs = Input(shape=(784, ))
nD1 = seq_model.layers[0](input2)
nD2 = seq_model.layers[1](nD1)
nD3 = seq_model.layers[2](nD2)
nD4 = seq_model.layers[3](nD3)
model1 = Model(input2, nD4) # input, output
model1compile(loss='categorical_crossentropy',
              optimizer=Adam(lr=1e-3, beta_1=0.9, beta_2=0.999, epsilon=1e-8),
              metrics=[metrics.categorical_accuracy])
model1.summary()

loss_and_metric = model1.evaluate(X_train, y_train, batch_size=128, verbose=0)
print('train, loss and metric: {}'.format(loss_and_metric))
loss_and_metric = model1.evaluate(X_test, y_test, batch_size=128, verbose=0)
print('test, loss and metric: {}'.format(loss_and_metric))
```
```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
input_35 (InputLayer)        (None, 784)               0         
_________________________________________________________________
dense_74 (Dense)             (None, 512)               401920    
_________________________________________________________________
dense_75 (Dense)             (None, 128)               65664     
_________________________________________________________________
dense_76 (Dense)             (None, 32)                4128      
_________________________________________________________________
dense_77 (Dense)             (None, 10)                330       
=================================================================
Total params: 472,042
Trainable params: 472,042
Non-trainable params: 0
_________________________________________________________________
train, loss and metric: [0.041054270681467921, 0.98849090910824866]
test, loss and metric: [0.078584650909528139, 0.97660000000000002]
```
## multi-input and multi-output
- 여러 input과 output이 함께 들어오는 뉴럴넷을 설계
- multi input은 `keras.layers.concatenate`를 이용해서 합침
- multi input/output은 fitting할 때, name을 key로 넘겨줘야 함. 따라서 name을 명확하게 명시할 것.
```python
import keras
from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model

# Headline input: meant to receive sequences of 100 integers, between 1 and 10000.
# Note that we can name any layer by passing it a "name" argument.
main_input = Input(shape=(100,), dtype='int32', name='main_input')

# This embedding layer will encode the input sequence
# into a sequence of dense 512-dimensional vectors.
x = Embedding(output_dim=512, input_dim=10000, input_length=100)(main_input)

# A LSTM will transform the vector sequence into a single vector,
# containing information about the entire sequence
lstm_out = LSTM(32)(x)

auxiliary_output = Dense(1, activation='sigmoid', name='aux_output')(lstm_out)

auxiliary_input = Input(shape=(5,), name='aux_input')
# concatenate inputs
x = keras.layers.concatenate([lstm_out, auxiliary_input])

# We stack a deep densely-connected network on top
x = Dense(64, activation='relu')(x)
x = Dense(64, activation='relu')(x)
x = Dense(64, activation='relu')(x)

# And finally we add the main logistic regression layer
main_output = Dense(1, activation='sigmoid', name='main_output')(x)

model = Model(inputs=[main_input, auxiliary_input], outputs=[main_output, auxiliary_output])

model.compile(optimizer='rmsprop', loss='binary_crossentropy',
              loss_weights=[1., 0.2])
"""
model.fit({'main_input': headline_data, 'aux_input': additional_data}, 
          {'main_output': labels, 'aux_output': labels}, 
          epochs=50, batch_size=32)
"""
model.summary()
```
```
____________________________________________________________________________________________________
Layer (type)                     Output Shape          Param #     Connected to                     
====================================================================================================
main_input (InputLayer)          (None, 100)           0                                            
____________________________________________________________________________________________________
embedding_3 (Embedding)          (None, 100, 512)      5120000     main_input[0][0]                 
____________________________________________________________________________________________________
lstm_3 (LSTM)                    (None, 32)            69760       embedding_3[0][0]                
____________________________________________________________________________________________________
aux_input (InputLayer)           (None, 5)             0                                            
____________________________________________________________________________________________________
concatenate_2 (Concatenate)      (None, 37)            0           lstm_3[0][0]                     
                                                                   aux_input[0][0]                  
____________________________________________________________________________________________________
dense_85 (Dense)                 (None, 64)            2432        concatenate_2[0][0]              
____________________________________________________________________________________________________
dense_86 (Dense)                 (None, 64)            4160        dense_85[0][0]                   
____________________________________________________________________________________________________
dense_87 (Dense)                 (None, 64)            4160        dense_86[0][0]                   
____________________________________________________________________________________________________
main_output (Dense)              (None, 1)             65          dense_87[0][0]                   
____________________________________________________________________________________________________
aux_output (Dense)               (None, 1)             33          lstm_3[0][0]                     
====================================================================================================
Total params: 5,200,610
Trainable params: 5,200,610
Non-trainable params: 0
____________________________________________________________________________________________________
```
- 그림으로 보기
```python
from IPython.display import SVG # jupyter notebook에서 보려고
from keras.utils.vis_utils import model_to_dot # keras model을 dot language로 변환
from keras.utils import plot_model

plot_model(model1, to_file='YOUR_FILE_PATH')
SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg')
```
출처: https://frhyme.github.io/machine-learning/a_model_in_keras/
