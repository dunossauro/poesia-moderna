from json import load
from random import choice
from verbos import Indicativo

with open('gramatica.json') as file:
    gramatica = load(file)

with open('esquemas_frases.json') as file:
    esquemas = load(file)

# Dicionário com a definição para as palavras de gênero e número
DIC = {'art_def_mas_sin' : gramatica['art_def_mas_sin'],
       'sub_com_mas_sin': choice(gramatica['sub_com_mas_sin']),
       'adj_sim_mas': '{}o'.format(choice(gramatica['adj_sim'])),
       'adv': choice(gramatica['adv']),
       'art_def_fem_sin': choice(gramatica['art_def_fem_sin']),
       'sub_com_fem_sin': choice(gramatica['sub_com_fem_sin']),
       'adj_sim_fem': '{}a'.format(choice(gramatica['adj_sim'])),
       'adj_sim_mas_plu': '{}os'.format(choice(gramatica['adj_sim'])),
       'art_def_mas_plu': gramatica['art_def_mas_plu'],
       'sub_com_mas_plu': '{}s'.format(choice(gramatica['sub_com_mas_sin']))}


def ter_pre_ind(numero, verbo):
    """
    Define um tempo aleatório no indicativo e responde baseado
        em número

    Args:
        - numero: Recebe um átomo gramatical para número
        - verbo: verbo a ser flexionado pela classe
    """
    ind = Indicativo(verbo)
    numero = numero[-3:]
    tempos_indicativo = [ind.presente,
                         ind.pret_per,
                         ind.pret_imper,
                         ind.pret_maisque,
                         ind.futuro_pres,
                         ind.futuro_pret]

    tempo = choice(tempos_indicativo)
    if numero == 'sin':
        return tempo()['ela/ele']

    elif numero == 'plu':
        return tempo()['elas/eles']


def main():
    esquema = choice(list(esquemas.keys()))
    frase = []

    for gra in esquemas[esquema]:
        if gra == 'ver_uni':
            frase.append(ter_pre_ind(esquema,
                                     choice(gramatica[gra])))
        else:
            frase.append(DIC[gra])

    return ' '.join(frase)

print(main())
