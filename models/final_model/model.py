import sys
sys.path.append('models/')
#sys.path.append('models/decision_tree/')

from decision_tree.decision_tree import get_distribution as decision_tree
from model1.model1 import get_distribution as model1
from decision_tree.decision_tree import make_states as make_dt
from model1.model1 import make_states as make_m1

from tensorflow_probability import distributions as tfd
import tensorflow as tf
import numpy as np

DIRECTIONS = 'LRF'


def get_distribution(i,s,s1,mix=0.55):
    m1 = model1(s)
    dt = decision_tree(i,s1)
    return tfd.Mixture(
        cat=tfd.Categorical(probs=[mix, 1.-mix]),
        components=[m1,dt])

def model(input):
    states = make_m1(input)
    states1 = make_dt(input)
    directions = 'S'
    for i,s in enumerate(states):
        s1 = states1[i]
        dist = get_distribution(i,s,s1)
        directions += DIRECTIONS[dist.sample()]
    return directions
