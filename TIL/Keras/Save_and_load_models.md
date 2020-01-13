# Make Keras model
```python
import json
from keras.models import Sequential
...

model = Sequential()
...
model.compile(~)
model.fit(~)
```

# Model save
```python
model_json = model.to_json()
with open('model.json', 'w') as json_file:
    json_file.write(model_json)
```

# Model weight save
```python
model.save_weights('model.h5')
```

# Model load
```python
from keras.models import model_from_json

with open('model.json', 'r') as json_file:
    loaded_model_json = json_file.read()
loaded_model = model_from_json(loaded_model_json)
```

# Model load and evaluation
유의할 점은 model load 후 다시 `compile을` 해야 한다.
```python
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X, Y, verbose=0)
```


출처: http://www.kwangsiklee.com/2019/03/keras에서-모델-saveload하기/
