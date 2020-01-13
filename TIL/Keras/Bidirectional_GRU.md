# keras model 생성
- 출처: https://github.com/Dark-Sied/Intent_Classification/blob/master/Intent_classification_final.ipynb
```python
from keras.models import Sequential
from keras.layers import Embedding, Dense, GRU, Bidirectional, BatchNormalization, Dropout

def create_model(vocab_size, input_length, num_classes):
    model = Sequential()
    
    model.add(Embedding(vocab_size, 128,
              input_length=input_length, trainable=False))
    model.add(Bidirectional(GRU(128))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(BatchNormalization())
    model.add(Dense(num_classes, activation='softmax'))
    
    return model

VOCAB_SIZE = 5000
INPUT_LENGTH = X.shape[1] # 32206
NUM_CLASSES = 814

model = create_model(vocab_size=VOCAB_SIZE, 
                     input_length=INPUT_LENGTH,
                     num_classes=NUM_CLASSES)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
```
