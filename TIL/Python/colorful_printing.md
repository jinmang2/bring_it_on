# colorful printing

```python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    pass_str = OKGREEN + 'Pass' + ENDC
    fail_str = FAIL + 'Fail' + ENDC
    

def print_warning(*args):
    s = ' '.join(args)
    print(bcolors.WARNING + '{}'.format(s) + bcolors.ENDC)


def print_green(*args):
    s = ' '.join(args)
    print(bcolors.OKGREEN + '{}'.format(s) + bcolors.ENDC)


def print_blue(*args):
    s = ' '.join(args)
    print(bcolors.OKBLUE + '{}'.format(s) + bcolors.ENDC)


def print_error(*args):
    s = ' '.join(args)
    print(bcolors.FAIL + '{}'.format(s) + bcolors.ENDC)
```

![image](https://user-images.githubusercontent.com/37775784/81642190-d4b93b80-945d-11ea-806c-d774c9c2edee.png)


출처: https://github.com/awslabs/w-lda/blob/master/npmi_calc.py
