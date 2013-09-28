def f(x):
    return x**2

def g():
    return 12

def e(*args):
    return sum(args)

d = {'a': [f, 2], 'b': g, 'c': [e, 2, 3]}
key = 'c'
if isinstance(d[key], list):
    h = d[key][0]
    args = d[key][1:]
    print h(*args)
else:
    h = d[key]
    print h()
