
from objects import Vector, H,P, Experiment
import numpy as np
import matplotlib.pyplot as plt
import re
import itertools

FRONT = Vector(0,1)
RIGHT = Vector(1,0)
LEFT = Vector(-1,0)

DIRECTIONS = {'F':FRONT,'R':RIGHT,'L':LEFT, 'S':Vector(0,0)}

R_90 = np.array([[0,1],[-1,0]]) 
L_90 = np.array([[0,-1],[1,0]]) 

def rotate_vector(vec,R):
    if np.all(vec.pos == RIGHT.pos):
        R = np.dot(R,R_90)
    if np.all(vec.pos == LEFT.pos):
        R = np.dot(R,L_90)
    return R

def make_experiment(cells,directions):
    cells = cells.upper()
    cells = re.sub(r'[^HP]+','',cells)
    directions = directions.upper()
    directions = re.sub(r'[^FRLS]+','',directions)
    
    experiment = Experiment()

    for i,cell in enumerate(cells):
        C = H() if cell == 'H' else P()
        d = np.dot(experiment.basis, DIRECTIONS[directions[i]].pos)
        D = Vector(d[0],d[1])
        experiment.add_Cell(C,D)
        experiment.basis = rotate_vector(DIRECTIONS[directions[i]],experiment.basis)

    return experiment
    

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
        if (count_P >=1 and count_H >= 2 * count_P):
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

#gera_inputs_V2([5,6,7])


def gera_gerador(input): #Recebe uma string e gera todas as possíveis combinações de R,L e F
    N = len(input)
    a = list(itertools.product('RLF',repeat = N-1))
    a_str = ['S' + ''.join(x) for x in a]
    return a_str
    

exp = make_experiment('HHHHHPPHH','SFRRFLLFF')
exp.count_energy()
print(exp.energy,exp.energies)
exp.plot_Experiment()
plt.show()