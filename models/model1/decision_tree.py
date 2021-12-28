import pandas as pd
import numpy as np

import tensorflow as tf
import tensorflow_probability as tfp
td = tfp.distributions

PROBS = pd.read_pickle('probs.pkl')
DIRECTIONS = 'LRF'

def get_distribution(state):
    probs = PROBS[state].values
    return td.Categorical(probs=probs)

def make_states(values):
    states = ['_'+values[:2]]
    for i,val in enumerate(values[1:-1]):
        states.append(values[i]+val+values[i+2])
    return states

def model(values):
    states = make_states(values)
    directions = 'S'
    for state in states:
        dist = get_distribution(state)
        directions += DIRECTIONS[dist.sample()]
    return directions