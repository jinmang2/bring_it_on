```python
import random
import numpy as np
import tensorflow as tf

# Assume that you have 12GB of GPU memory and want to allocate ~4GB:
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)

session_conf = tf.ConfigProto(intra_op_parallelism_threads=1,
                              inter_op_parallelism_threads=1,
                              # gpu_options=gpu_options,
                              )
session_conf.gpu_options.allow_growth = True # 탄력적으로 memory 사용

from keras import backend as K

random.seed(12345)
np.random.seed(42)
tf.set_random_seed(1234)

sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
K.set_session(sess)
```
