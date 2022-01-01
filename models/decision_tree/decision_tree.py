import numpy as np
import pandas as pd
import sys
sys.path.append('models/')

PATH = "models/decision_tree/"#'C:/Users/reasc/OneDrive - Universidade do Minho (1)/Mestrado/Primer Semestre/PP/Protein_Fold2D/models/decision_tree/'

PROBS = [pd.read_pickle(PATH + f'altura{i}.pkl') for i in range(6)]

import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions

FUNCTIONS = {}
for case in ['HH','HP','PH','PP']:
    FUNCTIONS[case] = pd.read_pickle(PATH + f'{case}.pkl')
DIRECTIONS = 'LRF'

def function(f):
    return lambda x: x*f['w'] + f['b'] + tfd.Normal(0,0.1).sample()

def get_distribution(i,state):
    if i < 6:
        probs = PROBS[i][state].values
    else:
        pL = function(FUNCTIONS[state])(i)[0]
        pL = 0.4 if pL > 0.4 else pL
        pL = 0.1 if pL < 0.1 else pL
        pR = pL
        pF = np.float32(1 - 2*pL)
        probs = [pL,pR,pF]
    return tfd.Categorical(probs=probs)

def make_states(values):
    states = []
    for i,val in enumerate(values[:-1]):
        states.append(val+values[i+1])
    return states

def model(values):
    states = make_states(values)
    directions = 'S'
    for i,state in enumerate(states):
        dist = get_distribution(i,state)
        directions += DIRECTIONS[dist.sample()]
    return directions
