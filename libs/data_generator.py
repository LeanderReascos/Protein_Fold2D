import itertools
import pandas as pd
from functions import make_experiment

def verifica_string(lista,tamanho):
    result = []
    count_H = 0
    count_P = 0
    for i in range(len(lista)):
        for j in range(tamanho):
            if (lista[i][j] == 'H'):
                count_H +=1
            elif (lista[i][j] == 'P'):
                count_P +=1
        if (count_P >=1 and count_H >= tamanho/2):
            result.append(lista[i])
        count_H = 0
        count_P = 0
    return result


def gera_inputs():

    a = list(itertools.product('HP', repeat = 5))
    b = list(itertools.product('HP', repeat = 6))
    c = list(itertools.product('HP', repeat = 7))

    inputs_5chars = verifica_string(a,5)
    inputs_6chars = verifica_string(b,6)
    inputs_7chars = verifica_string(c,7)

    inputs_total = [*inputs_5chars,*inputs_6chars,*inputs_7chars]

    inputs_total = [''.join(x) for x in inputs_total]

    print(inputs_total)


def gera_inputs_V2(N): #Recebe uma lista com os comprimentos das strings dos inputs
    lista = []         #Faz o mesmo que a gera_inputs() mas permite gerar os inputs com os caracteres que quisermos
    for i in range(len(N)):
        lista.append(verifica_string(list(itertools.product('HP',repeat = N[i])),N[i]))
    lista_total = [i for sublist in lista for i in sublist]
    lista_total = [''.join(x) for x in lista_total]
    return lista_total


def gera_gerador(input): #Recebe uma string e gera todas as possíveis combinações de R,L e F
    N = len(input)
    a = list(itertools.product('RLF',repeat = N-1))
    a_str = ['S' + ''.join(x) for x in a]
    return a_str

def generate_InputDataset(values):
    inputs = gera_inputs_V2(values)
    Inputs = []
    Directions = []
    for i in inputs:
        directions = gera_gerador(i)
        for direction in directions:
            Inputs.append(i)
            Directions.append(direction)
    
    df = pd.DataFrame()
    df['Inputs'] = Inputs
    df['Directions'] = Directions
    return df
    
def generate_Dataset(df):
    I = df['Inputs'].values
    D = df['Directions'].values
    energies = []
    inputs = []
    directions = []
    for i in range(len(df)):
        print(f'{i}/{len(df)}',end='\r')
        exp = make_experiment(I[i],D[i])
        if exp is not None:
            exp.count_energy()
            energies.append(exp.energy)
            inputs.append(I[i])
            directions.append(D[i])
    final = pd.DataFrame()
    final['Inputs'] = inputs
    final['Directions'] = directions
    final['Energy'] = energies
    return final

