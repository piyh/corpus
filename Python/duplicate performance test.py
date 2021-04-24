import random

def test_set(xs):
    seen = set()  # O(1) lookups
    for x in xs:
        if x not in seen:
            seen.add(x)
        else:
            return x

import collections

def test_counter(xs):
    freq = collections.Counter(xs)
    for k in freq:
        if freq[k] > 1:
            return k

def test_dict(xs):
    d = {}
    for x in xs:
        if x in d:
            return x
        d[x] = 1

def test_sort(xs):
    ys = sorted(xs)

    for n in range(1, len(xs)):
        if ys[n] == ys[n-1]:
            return ys[n]

##

import sys, timeit
print (sys.version + "\n")
xs = list(range(10000)) + [999]
random.shuffle(xs)
fns = [p for name, p in globals().items() if name.startswith('test')]
for fn in fns:
    assert fn(xs) == 999
    print ('%50s %.5f' % (fn, timeit.timeit(lambda: fn(xs), number=100)))
