# keras 모델 생성
- 출처: https://towardsdatascience.com/multi-class-text-classification-with-lstm-1590bee1bd17
```python
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D

# construct model
model = Sequential()
model.add(Embedding(MAX_VOCAB_SIZE, EMBEDDING_DIM, input_length=input_length))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(814, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

from keras.callbacks import EarlyStopping
EPOCHS = 5
BATCH_SIZE = 64

history = model.fit(X_train, y_train,
                    epochs=EPOCHS, batch_size=BATCH_SIZE,
                    validation_split=0.1,
                    callbacks=[
                        EarlyStopping(monitor='val_loss',
                                      patience=3,
                                      min_delta=0.0001)])
```
