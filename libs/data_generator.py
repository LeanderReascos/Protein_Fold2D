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
        if (count_P >=1 and count_H >= 3):
            result.append(lista[i])
        count_H = 0
        count_P = 0
    return result


def gera_inputs(N): 
    lista = []         
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
    inputs = gera_inputs(values)
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
            if exp.energy > 0:
                energies.append(exp.energy)
                inputs.append(I[i])
                directions.append(D[i])
    final = pd.DataFrame()
    final['Inputs'] = inputs
    final['Directions'] = directions
    final['Energy'] = energies
    return final

if __name__ == '__main__':
    args = [5,6,7,8]
    df = generate_InputDataset(args)
    print(len(df))
    final = generate_Dataset(df)
    final.to_csv('data/dataset.csv',index = False)