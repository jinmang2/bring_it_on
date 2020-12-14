from functools import reduce


def checkIBSN(sequence):
    func = lambda i, j: i + int(j[1]) * j[0]
    out = reduce(func, enumerate(sequence[:-1], start=1), 0) % 11
    out = out if out != 10 else 'X'
    return out == sequence[-1]


checkIBSN('123456789X')
>>> True
