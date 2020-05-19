# Linux에서 python 코드 원격 디버그

### Linux 컴퓨터 설정
- Mac OSX 또는 Linux와 같은 운영 체제에서 Python을 실행하는 원격 컴퓨터.
- 원격 디버깅의 기본값으로 해당 컴퓨터의 방화벽에서 열려 있는 포트 5678(인바운드).

### 예시 스크립트 준비
```python
import random
import ptvsd
ptvsd.enable_attach()

guesses_made = 0
name = input('Hello! What is your name?\n')
number = random.randint(1, 20)
print('Well, {0}, I am thinking of a number between 1 and 20.'.format(name))

while guesses_made < 6:
    guess = int(input('Take a guess: '))
    guesses_made += 1
    if guess < number:
        print('Your guess is too low.')
    if guess > number:
        print('Your guess is too high.')
    if guess == number:
        break
if guess == number:
    print('Good job, {0}! You guessed my number in {1} guesses!'.format(name, guesses_made))
else:
    print('Nope. The number I was thinking of was {0}'.format(number))
```

- https://docs.microsoft.com/ko-kr/visualstudio/python/debugging-python-code-on-remote-linux-machines?view=vs-2019
