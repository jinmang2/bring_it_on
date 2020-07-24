```python
from transformers import BertTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# BERT의 토크나이저로 문장을 토큰으로 분리
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case=False)
# BERT의 입력 형식에 맞게 변환
sentences_ = ["[CLS] " + str(sentence) + " [SEP]" for sentence in sentences]
# BERT의 토크나이저로 문장을 토큰으로 분리
tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences_]
# 토큰을 숫자 인덱스로 변환
input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]

# 문장을 MAX_LEN 길이에 맞게 자르고, 모자란 부분을 패딩 0으로 채움
input_ids = pad_sequences_keras(input_ids, maxlen=128, dtype="long", truncating="post", padding="post")

print(input_ids)
print(input_ids.shape)
```
```
[[  101  8911   100 ...     0     0     0]
 [  101   144 11490 ...     0     0     0]
 [  101  9303 21711 ...     0     0     0]
 ...
 [  101  8924 67527 ...     0     0     0]
 [  101  9666 14423 ...     0     0     0]
 [  101  9246 32537 ...     0     0     0]]

(50000, 128)
```
