from models.decision_tree.decision_tree import model as dt
from models.model1.decision_tree import model as m1
from libs.functions import make_experiment
import statistics

def compare_models(model,Input,N,max_iterations = 1500):
    dic = {}
    var = N
    directions = []
    energy = []
    count = 0
    n = 10
    while(n):
        direction = model(Input)
        exp = make_experiment(Input,direction)
        if exp is not None:
            exp.count_energy()
            if exp.energy > 0:
                energy.append(exp.energy)
                directions.append(direction)
                n -= 1
        count += 1
    average_energy = statistics.mean(energy)
    N -= 10
    while(N):
        n = 10
        while(n):
            direction = model(Input)
            exp = make_experiment(Input,direction)
            if exp is not None:
                exp.count_energy()
                if (exp.energy > average_energy):
                    energy.append(exp.energy)
                    directions.append(direction)
                    n -= 1
                print(str(len(energy)) + "/" + str(var))
            count += 1
        average_energy = statistics.mean(energy)
        N -=10
        if count >= max_iterations:
            break
    average_energy = statistics.mean(energy)
    standard_devi = statistics.stdev(energy)

    max_energy = max(energy)

    dic["direction"] = directions
    dic["energy"] = energy
    dic["mean_energy"] = average_energy
    dic["standard_devi"] = standard_devi
    dic["counts"] = count
    dic["max_energy"] = max_energy
    
    return dic

#print(compare_models(dt,"HPHPPHHPHPPHPHHPPHPH",20))




# Funcao (model,Input,N)
# ex = make_experiment(Input, resultado)
#  if exp is not None:
#       ex.count_energy()
#       ex.energy()
# max_energy, reults = [[Direcoes,Energia]]