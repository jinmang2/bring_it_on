# Unicode
https://docs.python.org/ko/3.7/howto/unicode.html

```python
>>> 'ㄱ'.encode('utf-8', 'ignore')
b'\xe3\x84\xb1'

>>> 's'.encode('utf-8', 'ignore')
b's'

>>> print("\N{GREEK CAPITAL LETTER DELTA}")
Δ

>>> "\u0394"
'Δ'

>>> "\U00000394"
'Δ'

>>> ord('ㄱ')
12593

>>> chr(12593)
'ㄱ'

>>> s = "a\xac\u1234\u20ac\U00008000"
>>> [ord(c) for c in s]
[97, 172, 4660, 8364, 32768]

>>> u = 'abcdé'
>>> print(ord(u[-1]))
233
```

```python
import unicodedata

u = chr(233) + chr(0x0bf2) + chr(3972) + chr(6000) + chr(13231)

for i, c in enumerate(u):
    print(i, '%04x' % ord(c), unicodedata.category(c), end=" ")
    print(unicodedata.name(c))

# Get numeric value of second character
print(unicodedata.numeric(u[1]))
```
```
0 00e9 Ll LATIN SMALL LETTER E WITH ACUTE
1 0bf2 No TAMIL NUMBER ONE THOUSAND
2 0f84 Mn TIBETAN MARK HALANTA
3 1770 Lo TAGBANWA LETTER SA
4 33af So SQUARE RAD OVER S SQUARED
1000.0
```

```python
>>> street = 'Gürzenichstraße'
>>> street.casefold() # case-insensitive comparision
'gürzenichstrasse'
```

```python
import unicodedata

def compare_strs(s1, s2):
    def NFD(s):
        return unicodedata.normalize('NFD', s)

    return NFD(s1) == NFD(s2)

single_char = 'ê'
multiple_chars = '\N{LATIN SMALL LETTER E}\N{COMBINING CIRCUMFLEX ACCENT}'
print('length of first string=', len(single_char))
print('length of second string=', len(multiple_chars))
print(compare_strs(single_char, multiple_chars))
```
```
length of first string= 1
length of second string= 2
True
```

```python
import unicodedata

def compare_caseless(s1, s2):
    def NFD(s):
        return unicodedata.normalize('NFD', s)

    return NFD(NFD(s1).casefold()) == NFD(NFD(s2).casefold())

# Example usage
single_char = 'ê'
multiple_chars = '\N{LATIN CAPITAL LETTER E}\N{COMBINING CIRCUMFLEX ACCENT}'

print(compare_caseless(single_char, multiple_chars))
```
```
True
```

```python
fn = 'filename\u4500abc'
f = open(fn, 'w')
f.close()

import os
print(os.listdir(b'.'))
print(os.listdir('.'))
```
```
[b'.ipynb_checkpoints', b'200330_studying.ipynb', b'ELMo_biLM_layer.ipynb', b'ELMo_char-CNN_layer.ipynb', b'ELMo_layer.ipynb', b'ELMO_tokenize_and_create_batches.ipynb', b'filename\xe4\x94\x80abc', b'mask[0].pt', b'mask[1].pt', b'mask[2].pt', b'python_overrides.ipynb', b'testing_ELMo_biLM_layer.ipynb', b'token_embedding.pt', b'Untitled.ipynb']
['.ipynb_checkpoints', '200330_studying.ipynb', 'ELMo_biLM_layer.ipynb', 'ELMo_char-CNN_layer.ipynb', 'ELMo_layer.ipynb', 'ELMO_tokenize_and_create_batches.ipynb', 'filename䔀abc', 'mask[0].pt', 'mask[1].pt', 'mask[2].pt', 'python_overrides.ipynb', 'testing_ELMo_biLM_layer.ipynb', 'token_embedding.pt', 'Untitled.ipynb']
```

```python
import codecs

new_f = codecs.StreamRecoder(f,
    # en/decoder: used by read() to encode its results and
    # by write() to decode its input.
    codecs.getencoder('utf-8'), codecs.getdecoder('utf-8'),

    # reader/writer: used to read and write to the stream.
    codecs.getreader('latin-1'), codecs.getwriter('latin-1') )
```

