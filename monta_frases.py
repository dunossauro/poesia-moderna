from json import load
from random import choice
from verbos import Indicativo

with open('gramatica.json') as file:
    gramatica = load(file)

with open('esquemas_frases.json') as file:
    esquemas = load(file)


def ter_pre_ind(esquema, verbo):
    ind = Indicativo(verbo)
    tempos_indicativo = [ind.presente,
                         ind.pret_per,
                         ind.pret_imper,
                         ind.pret_maisque,
                         ind.futuro_pres,
                         ind.futuro_pret]

    tempo = choice(tempos_indicativo)
    if esquema[0][-3:] == 'sin':
        return tempo()['ela/ele']

    elif esquema[0][-3:] == 'plu':
        return tempo()['elas/eles']


def frases():
    esquema = choice(list(esquemas.keys()))
    frase = []

    for x in esquemas[esquema]:
        if type(gramatica[x]) is list:
            if 'ver' in x:
                frase.append(ter_pre_ind(esquemas[esquema], choice(gramatica[x])))
            else:
                frase.append(choice(gramatica[x]))
        else:
            frase.append(gramatica[x])

    return ' '.join(frase)

print(frases())
