from re import compile
from string import ascii_uppercase
from itertools import count

c = count(0)

regex_p = compile(r'palavra:(.*)\ndivisão:(.*)\n')

for x in ascii_uppercase:
    with open('{}.txt'.format(x)) as a:
        palavras = regex_p.findall(a.read())

    for x in palavras:
        print(x[0], x[1])
