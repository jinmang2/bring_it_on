# First contact with TensorFlow Estimator
이 문서는 [First contact with TensorFlow Estimator](https://towardsdatascience.com/first-contact-with-tensorflow-estimator-69a5e072998d)를 학습 후 기록용으로 남기는 문서입니다.

또한 [원문] 해당 포스트는 저자가 [Barcelona Supercomputing Center](https://www.upc.edu/en?set_language=en)의 지원을 받아 저자의 석사 코스 SA-MIRI at [UPC Barcelona Tech](https://www.upc.edu/en?set_language=en)에서 사용될 예정이라고 밝혔습니다.

그럼 시작합니다.

## TensorFlow가 제공하는 다양한 API들을 stack 형태로 보자
![Null](https://miro.medium.com/max/1872/1*8e8Aq_GlJFy8tGuZx1F2IA.png)
Source: https://www.tensorflow.org/get_started/premade_estimators

- High vs Low level API
- 나는 `Bidirectional Encoder Representations from Transformers(BERT)`의 `model_fn_build` 함수를 파헤치고 싶었음
- 때문에 High-Level TensorFlow APIs `Estimators`에 관심이 많았는데 이 문서에서 이에 대한 내용을 다룸
- 추가적인 설명을 덧붙이자면, 대부분의 lower level에서
    - `Tensorflow`는 `Node`가 계산 단위이고 `Edge`가 `Tensor`(다차원 배열)의 흐름인 `Graph`를 통한 데이터 흐름으로 일련의 계산에 접근
    - `Tensorflow`는 실행하기 전 계산 그래프를 빌드함(2.0에선 graph말고 바로 실행가능한 모드도 생겼죠!)
    - `Graph`는 node가 정의되도 실행되지 않음. 계산은 필요한 경우에만 schedule됨(lazy execution)
    - `Graph`가 assemble된 후에 실행되는 하드웨어를 바인딩하는 런타임 환경인 `Session`에서 전개 & 실행됨
- `TensorFlow`는 TensorBoard로 computation graph를 시각화할 수 있음

## TensorFlow Estimators overview
- `TensorFlow`의 `Estimators`는 2017년 (White paper)[https://arxiv.org/abs/1708.02637]에서 소개된 ML 프로그래밍을 굉장히 단순화시킨 High-Level TensorFlow API
- Design Goal is as follows:
    - automating reetitive and error-prone tasks(반복적이고 오류가 발생하기 쉬운 작업 자동화)
    - encapsulating best practices(최고의 실험 캡슐화)
        - `Encapsulation` In OOP
            1. 객체의 속성(data fields)과 행위(methods)를 하나로 묶고
            2. 실제 구현 내용 일부를 외부에 감춰 은닉
    - providing a ride from training to deployment(학습부터 배포까지 제공)
- TRAIN, EVALUATE, TEST를 아주 간편하게 configure하는 고수준 API
- 추가적인 이점
    - 모델을 reordering하지 않고 CPU, GPU, TPU에서 구동 가능
    - 학습 loop 중에 다음의 활동들을 안전하게 분산처리가 가능
        - build a graph
        - initialize variables
        - start queues
        - create checkpoints
        - save summaries to Tensorboard
    - 서비스 제공

#### Pre-made Estimators
- `tf.estimator.Estimator` 클래스에서 미리 구현된 네트워크 존재
- 꺼지셈 나는 직접 짤거심!

#### Estimators Interface
- `scikit-learn`과 유사하게 **train-evaluate*predict**의 interface를 지님
- user는 TRAIN, EVALUATE, 그리고 PREDICT간에 다른 동작을 시키는 조건을 사용하여 모델을 구축
![None](https://miro.medium.com/max/1062/1*LF9lKi-LaNRwyL5lLfKRNg.png)

#### Custom Estimator minimum layout
- 고수준 API에서, custom Estimator(`tf.estimator.Estimator`)을 만드려면
    - `model_fn` 함수를 정의
        - input: `features`, `labels`, other parameters
        - in code: `model`, `loss`, `optimizer`, `metric` 내부에서 정의 or 호출
        - output: `tf.estimator.EstimatorSpec`
    - `train_input_fn', 'eval_input_fn` 정의
    - An experiment object
- 더 자세한 내용은 [여기](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/18d86099a350df93f2bd88587c0ec6d118cc98e7.pdf) 참고.

## Time to get your hands dirty!
```python
# Import Libraries
import os, sys, time
import numpy as np
import tensorflow as tf

# Store basic params
_NUM_CLASSES = 10
_MODEL_DIR = 'model_name'
_NUM_CHANNELS = 1
_IMG_SIZE = 28
_LEARNING_RATE = 0.05
_NUM_EPOCHS = 20
_BATCH_SIZE = 2048

# Define Model
class Model:
    """MNIST CLASSIFIER"""
    def __call__(self, inputs):
        """
        The CNN Network below works when the Model object is called.
        #
        # input image size: [
        #                      n,   # batch_size
        #                      28,  # widths
        #                      28,  # heishts
        #                      3    # number of channels
        #                   ]
        # 
        # % convolution layer output size:
        #     OutputHeight = ceil[ (H + 2P - FH) / S ] + 1
        #     OutputWidth  = ceil[ (W + 2P - FW) / S ] + 1
        #                   where H : Images Height
        #                         FH: Filter Height
        #                         W : Images Width
        #                         FW: Filter Width
        #                         S : Strides
        #                         P : 0              if   padding =='VALID'
        #                             ceil[ FH / 2 ] elif padding =='SAME'
        #                         ceil: maps x to the least integer greater than or equal to x
        #
        # % pooling layer output size:
        #     OutputHeight = ceil[ (H + 2P - FH) / S ] + 1
        #     OutputWidth  = ceil[ (W + 2P - FW) / S ] + 1
        #
        # ------------------------------------------------------------------------------------
        # First Block is {
        #                  conv2d: {filter: [5, 5], 
        #                           channels: 32},
        #                  max_pool2d: {filter: [2, 2], 
        #                               stride: 2, 
        #                               padding:VALID} # Do not pad
        #                }
        #
        # 1 Batch is processed simultaneously by matrix operation!
        # - Conv2d layer:
        #    W==H==28, channel==3
        #    FW==FH==5, num_filter==32, S==1, Padding=="VALID"
        #    So, OW = OH = ceil[ (28 + 0 - 5) / 1 ] + 1 = 24
        #    Hence, return is [n, 24, 24, 32] where n is batch_size
        # - MaxPool2d layer:
        #    W==H==24, channel==32
        #    FW==FH==2, S==2
        #    So, OW = OH = ceil[ (24 - 2) / 2 ] + 1 = 12
        #    Hence, return is [n, 12, 12, 32] where n is batch_size
        #
        # ------------------------------------------------------------------------------------
        # Second Block is {
        #                   conv2d: {filter: [5, 5], 
        #                            channels: 64},
        #                   max_pool2d: {filter: [2, 2], 
        #                                stride: 2, 
        #                                padding:VALID} # Do not pad
        #                 }
        #
        # 1 Batch is processed simultaneously by matrix operation!
        # - Conv2d layer:
        #    W==H==12, channel==32
        #    FW==FH==5, num_filter==64, S==1, Padding=="VALID"
        #    So, OW = OH = ceil[ (12 + 0 - 5) / 1 ] + 1 = 8
        #    Hence, return is [n, 8, 8, 64] where n is batch_size
        # - MaxPool2d layer:
        #    W==H==8, channel==64
        #    FW==FH==2, S==2
        #    So, OW = OH = ceil[ (8 - 2) / 2 ] + 1 = 4
        #    Hence, return is [n, 4, 4, 64] where n is batch_size
        #
        # ------------------------------------------------------------------------------------
        # Third Block is Flatten layer
        #                  [n, 4, 4, 64] -|> [n, 4 * 4 * 64]
        #   Output size is [n, 1024]
        #
        # ------------------------------------------------------------------------------------
        # Finally, Fully Connected layer:
        #                  [n, 1024] -|> [n, 10]
        """
        # First Block
        net = tf.layers.conv2d(inputs, 32, [5, 5],
                               activation=tf.nn.relu, name='conv1')
        net = tf.layers.max_pooling2d(net, [2, 2], 2,
                                      name='pool1')
        # Second Block
        net = tf.layers.conv2d(net, 64, [5, 5],
                               activation=tf.nn.relu, name='conv2')
        net = tf.layers.max_pooling2d(net, [2, 2], 2,
                                      name='pool2')
        # Flatten layer
        net = tf.layers.flatten(net)
        # FC layer
        logits = tf.layers.dense(net, _NUM_CLASSES,
                                 activation=None, name='fc1')
        return logits

# Define `model_fn` function
def model_fn(features, labels, mode):
    """
    <MAIN FUNCTION OF THE TENSORFLOW ESTIMATOR API>
    
    Description:
        Function that sets up the internal graph to build
        and run our model
        and returns back the training and loss ops,
        along with any hooks.
    
    where:
        `features`: items returned from input_fn
        `labels`: second item returned from input_fn
        `mode`: the mode the estimator is running in
                (basically training, validation or prediction).
                
    the `mode` parameter can take one of three values:
        `tf.estimator.ModeKeys.TRAIN`
        `tf.estimator.ModeKeys.EVAL`
        `tf.estimator.ModeKeys.PREDICT`
        
    Return:
        `tf.estimator.EstimatorSpec` object.
        that contains:
            - the train/loss ops for training
            - loss and metrics for evaluation
            - precistions for inference
    
    reference:
        https://towardsdatascience.com/first-contact-with-tensorflow-estimator-69a5e072998d
    """
    model = Model() # Generate CNN Graph
    global_step = tf.train.get_global_step()
    
    # Reshape features to images
    images = tf.reshape(features, [-1, _IMG_SIZE, _IMG_SIZE, _NUM_CHANNELS])
    
    # Model Call and Operate CNN Layer using our images
    logits = model(images)
    # Get predicted class label from rows
    # (n, 10), n is batch_size and 10 is num_of_classes
    # argmax on axis=1 reduces 10 dimension to 1 that is predicted label
    # return size is (n, )
    predicted_logit = tf.argmax(input=logits, axis=1,
                                output_type=tf.int32)
    # For get a probabilities, apply softmax function to logits
    probabilities = tf.nn.softmax(logits)
    
    # case: PREDICT
    # For prediction, compile predictions in a dict
    predictions = {
        'predicted_logit': predicted_logit,
        'probabilities': probabilities
    }
    # Return an `EstimatorSpec` object
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)
    
    # Calculate loss for training and evaluation using cross-entropy
    with tf.name_scope('loss'):
        cross_entropy = tf.losses.sparse_softmax_cross_entropy(
            labels=labels, logits=logits, scope='loss')
        tf.summary.scalar('accuracy', cross_entropy) # for VISUALIZATION with TENSORBORAD
    # Accuracy metric for evaluate
    with tf.name_scope('accuracy'):
        accuracy = tf.metrics.accuracy(
            labels=labels, predictions=predicted_logit, name='acc')
        tf.summary.scalar('accuracy', accuracy[1]) # for VISUALIZATION with TENSORBORAD
        
    # case: EVALUATION
    if mode == tf.estimator.ModeKeys.EVAL:
        return tf.estimator.EstimatorSpec(mode=mode,
                                          loss=cross_entropy,
                                          eval_metric_ops={'accuracy/accuracy': accuracy},
                                          evaluation_hooks=None)
    # Create a SGD(Stochastic Gradient Descent) optimizer 
    optimizer = tf.train.GradientDescentOptimizer(
        learning_rate=_LEARNING_RATE)
    train_op = optimizer.minimize(cross_entropy,
                                  global_step=global_step)
    
    # In order to visualize the training process with Tensorboird,
    # create a hook to print acc, loss & global step every 100 iterations.
    train_hook_list = []
    train_tensors_log = {'accuracy': accuracy[1],
                         'loss': cross_entropy,
                         'global_step': global_step}
    train_hook_list.append(
        tf.train.LoggingTensorHook(tensors=train_tensors_log,
                                   every_n_iter=100)
    )
    ## Logging
    # Logging is useful for debugging long-running training sessions or processes
    # servicing inferences. Tensorflow supports the usual logging mechanism,
    # with 5 levels in order to increasing severity as follows:
    #   - DEBUG
    #   - INFO
    #   - WARN
    #   - ERROR
    #   - FATAL
    # You can set the log level in the probram by:
    # `tf.logging.set_verbosity(tf.logging.INFO)`
    
    # case: TRAIN
    if mode == tf.estimator.ModeKeys.TRAIN:
        return tf.estimator.EstimatorSpec(mode=mode,
                                          loss=cross_entropy,
                                          train_op=train_op,
                                          training_hooks=train_hook_list)
                                          
# Load Training and Test Data
mnist = tf.contrib.learn.datasets.load_dataset("mnist")
train_data = mnist.train.images # Returns a np.array
train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
eval_data = mnist.test.images # Returns a np.array
eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

# Input function to train the model
train_input_fn = tf.estimator.inputs.numpy_input_fn(x=train_data,
                                                    y=train_labels,
                                                    batch_size=_BATCH_SIZE,
                                                    num_epochs=1,
                                                    shuffle=True)

# Input function to evaluate the model
eval_input_fn = tf.estimator.inputs.numpy_input_fn(x=eval_data,
                                                   y=eval_labels,
                                                   num_epochs=1,
                                                   shuffle=False)

# Create teh Estimator
image_classifier = tf.estimator.Estimator(model_fn=model_fn, model_dir=_MODEL_DIR)

for _ in range(_NUM_EPOCHS):
    image_classifier.train(input_fn=train_input_fn)
    metrics = image_classifier.evaluate(input_fn=eval_input_fn)
```
```
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-27
WARNING:tensorflow:From C:\Users\jinma\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\tensorflow_core\python\training\saver.py:1069: get_checkpoint_mtimes (from tensorflow.python.training.checkpoint_management) is deprecated and will be removed in a future version.
Instructions for updating:
Use standard file utilities to get mtimes.
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 27 into model_name\model.ckpt.
INFO:tensorflow:loss = 1.847903, step = 27
INFO:tensorflow:accuracy = 0.6611328, global_step = 27, loss = 1.847903
INFO:tensorflow:Saving checkpoints for 54 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.87577367.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:07Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-54
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:07
INFO:tensorflow:Saving dict for global step 54: accuracy/accuracy = 0.76, global_step = 54, loss = 0.8908232
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 54: model_name\model.ckpt-54
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-54
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 54 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.9371305, step = 54
INFO:tensorflow:accuracy = 0.75341797, global_step = 54, loss = 0.9371305
INFO:tensorflow:Saving checkpoints for 81 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.5595695.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:09Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-81
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:09
INFO:tensorflow:Saving dict for global step 81: accuracy/accuracy = 0.8693, global_step = 81, loss = 0.45442674
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 81: model_name\model.ckpt-81
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-81
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 81 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.4702479, step = 81
INFO:tensorflow:accuracy = 0.8745117, global_step = 81, loss = 0.4702479
INFO:tensorflow:Saving checkpoints for 108 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.3972193.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:10Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-108
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:11
INFO:tensorflow:Saving dict for global step 108: accuracy/accuracy = 0.9123, global_step = 108, loss = 0.3215254
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 108: model_name\model.ckpt-108
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-108
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 108 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.36056423, step = 108
INFO:tensorflow:accuracy = 0.90283203, global_step = 108, loss = 0.36056423
INFO:tensorflow:Saving checkpoints for 135 into model_name\model.ckpt.
WARNING:tensorflow:From C:\Users\jinma\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\tensorflow_core\python\training\saver.py:963: remove_checkpoint (from tensorflow.python.training.checkpoint_management) is deprecated and will be removed in a future version.
Instructions for updating:
Use standard file APIs to delete files with this prefix.
INFO:tensorflow:Loss for final step: 0.31628627.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:12Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-135
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:12
INFO:tensorflow:Saving dict for global step 135: accuracy/accuracy = 0.9134, global_step = 135, loss = 0.30040425
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 135: model_name\model.ckpt-135
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-135
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 135 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.361807, step = 135
INFO:tensorflow:accuracy = 0.88964844, global_step = 135, loss = 0.361807
INFO:tensorflow:Saving checkpoints for 162 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.26667774.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:13Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-162
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:14
INFO:tensorflow:Saving dict for global step 162: accuracy/accuracy = 0.9293, global_step = 162, loss = 0.24614155
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 162: model_name\model.ckpt-162
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-162
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 162 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.27779824, step = 162
INFO:tensorflow:accuracy = 0.91748047, global_step = 162, loss = 0.27779824
INFO:tensorflow:Saving checkpoints for 189 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.3027214.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:15Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-189
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:15
INFO:tensorflow:Saving dict for global step 189: accuracy/accuracy = 0.9369, global_step = 189, loss = 0.2200433
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 189: model_name\model.ckpt-189
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-189
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 189 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.2388028, step = 189
INFO:tensorflow:accuracy = 0.93310547, global_step = 189, loss = 0.2388028
INFO:tensorflow:Saving checkpoints for 216 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.26855737.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:16Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-216
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:17
INFO:tensorflow:Saving dict for global step 216: accuracy/accuracy = 0.9403, global_step = 216, loss = 0.20338206
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 216: model_name\model.ckpt-216
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-216
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 216 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.2354249, step = 216
INFO:tensorflow:accuracy = 0.91796875, global_step = 216, loss = 0.2354249
INFO:tensorflow:Saving checkpoints for 243 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.19094676.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:18Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-243
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:18
INFO:tensorflow:Saving dict for global step 243: accuracy/accuracy = 0.9423, global_step = 243, loss = 0.19609627
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 243: model_name\model.ckpt-243
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-243
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 243 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.20120308, step = 243
INFO:tensorflow:accuracy = 0.9394531, global_step = 243, loss = 0.20120308
INFO:tensorflow:Saving checkpoints for 270 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.19384497.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:20Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-270
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:20
INFO:tensorflow:Saving dict for global step 270: accuracy/accuracy = 0.9446, global_step = 270, loss = 0.1856813
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 270: model_name\model.ckpt-270
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-270
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 270 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.19139485, step = 270
INFO:tensorflow:accuracy = 0.9433594, global_step = 270, loss = 0.19139485
INFO:tensorflow:Saving checkpoints for 297 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.14085837.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:21Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-297
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:21
INFO:tensorflow:Saving dict for global step 297: accuracy/accuracy = 0.9516, global_step = 297, loss = 0.16320045
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 297: model_name\model.ckpt-297
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-297
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 297 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.18372276, step = 297
INFO:tensorflow:accuracy = 0.94433594, global_step = 297, loss = 0.18372276
INFO:tensorflow:Saving checkpoints for 324 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.17227407.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:23Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-324
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:23
INFO:tensorflow:Saving dict for global step 324: accuracy/accuracy = 0.9531, global_step = 324, loss = 0.15785311
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 324: model_name\model.ckpt-324
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-324
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 324 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.18036121, step = 324
INFO:tensorflow:accuracy = 0.9458008, global_step = 324, loss = 0.18036121
INFO:tensorflow:Saving checkpoints for 351 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.17602293.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:24Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-351
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:24
INFO:tensorflow:Saving dict for global step 351: accuracy/accuracy = 0.953, global_step = 351, loss = 0.15291294
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 351: model_name\model.ckpt-351
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-351
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 351 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.14845657, step = 351
INFO:tensorflow:accuracy = 0.9584961, global_step = 351, loss = 0.14845657
INFO:tensorflow:Saving checkpoints for 378 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.18911296.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:26Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-378
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:26
INFO:tensorflow:Saving dict for global step 378: accuracy/accuracy = 0.9588, global_step = 378, loss = 0.14463677
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 378: model_name\model.ckpt-378
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-378
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 378 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.13643809, step = 378
INFO:tensorflow:accuracy = 0.95996094, global_step = 378, loss = 0.13643809
INFO:tensorflow:Saving checkpoints for 405 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.15499799.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:27Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-405
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:28
INFO:tensorflow:Saving dict for global step 405: accuracy/accuracy = 0.9605, global_step = 405, loss = 0.13333617
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 405: model_name\model.ckpt-405
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-405
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 405 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.16514203, step = 405
INFO:tensorflow:accuracy = 0.95214844, global_step = 405, loss = 0.16514203
INFO:tensorflow:Saving checkpoints for 432 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.14886652.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:29Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-432
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:29
INFO:tensorflow:Saving dict for global step 432: accuracy/accuracy = 0.9611, global_step = 432, loss = 0.12945421
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 432: model_name\model.ckpt-432
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-432
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 432 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.15450218, step = 432
INFO:tensorflow:accuracy = 0.9550781, global_step = 432, loss = 0.15450218
INFO:tensorflow:Saving checkpoints for 459 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.14768948.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:30Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-459
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:31
INFO:tensorflow:Saving dict for global step 459: accuracy/accuracy = 0.9623, global_step = 459, loss = 0.12590744
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 459: model_name\model.ckpt-459
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-459
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 459 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.14525445, step = 459
INFO:tensorflow:accuracy = 0.953125, global_step = 459, loss = 0.14525445
INFO:tensorflow:Saving checkpoints for 486 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.107749045.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:32Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-486
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:32
INFO:tensorflow:Saving dict for global step 486: accuracy/accuracy = 0.9634, global_step = 486, loss = 0.11967938
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 486: model_name\model.ckpt-486
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-486
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 486 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.1497466, step = 486
INFO:tensorflow:accuracy = 0.95947266, global_step = 486, loss = 0.1497466
INFO:tensorflow:Saving checkpoints for 513 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.14507939.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:34Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-513
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:34
INFO:tensorflow:Saving dict for global step 513: accuracy/accuracy = 0.9637, global_step = 513, loss = 0.11832073
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 513: model_name\model.ckpt-513
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-513
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 513 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.12068131, step = 513
INFO:tensorflow:accuracy = 0.9633789, global_step = 513, loss = 0.12068131
INFO:tensorflow:Saving checkpoints for 540 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.16064204.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:35Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-540
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:35
INFO:tensorflow:Saving dict for global step 540: accuracy/accuracy = 0.9669, global_step = 540, loss = 0.115646206
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 540: model_name\model.ckpt-540
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-540
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Saving checkpoints for 540 into model_name\model.ckpt.
INFO:tensorflow:loss = 0.12224751, step = 540
INFO:tensorflow:accuracy = 0.9692383, global_step = 540, loss = 0.12224751
INFO:tensorflow:Saving checkpoints for 567 into model_name\model.ckpt.
INFO:tensorflow:Loss for final step: 0.11171985.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2020-02-07T14:21:37Z
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from model_name\model.ckpt-567
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Finished evaluation at 2020-02-07-14:21:37
INFO:tensorflow:Saving dict for global step 567: accuracy/accuracy = 0.967, global_step = 567, loss = 0.1097073
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 567: model_name\model.ckpt-567
```
