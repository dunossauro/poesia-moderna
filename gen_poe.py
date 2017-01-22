from json import load
from random import choice
poem = []

with open('base.json') as file:
    dic = load(file)


def get_words(pos):
    poem.append(choice(dic[pos]))


def get_poem(pos):
    titulo = choice(dic[pos])
    for ele in titulo:
        if '<' in ele:
            get_words(ele[1:-1])
        else:
            poem.append(ele)


for ele in dic['poem']:
    if '<' in ele:
        get_poem(ele[1:-1])
    else:
        poem.append(ele)

print(' '.join(poem))
