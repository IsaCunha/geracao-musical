from deap import base, creator, tools
from fitness import *
import random

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

IND_SIZE = 128

toolbox = base.Toolbox()

ESCALA_MAIOR = [55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79]

def gerar_nota():
    # as músicas guias selecionadas vão de 60 a 75,
    # para a nota gerada aleatoriamente deixamos um limite com +/-5
    #return random.randint(60, 75)
    return random.choice(ESCALA_MAIOR)

toolbox.register("attribute", gerar_nota)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individuo):
    fitness_ind = calcular_fitness(individuo, conjunto_guias)
    return (fitness_ind,)

def mut_escala(individual, indpb):
    for i in range(len(individual)):
        if random.random() < indpb and individual[i] != 0:
            individual[i] = random.choice(ESCALA_MAIOR)
    return (individual,)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mut_escala, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=10)
toolbox.register("evaluate", evaluate)

def mut_silence(individual, indpb):
    for i in range(len(individual)):
        if random.random() < indpb and individual[i] != 0:
            individual[i] = 0
    return (individual,)

# Adiciona silencios entre a melodia
toolbox.register("mut_silence", mut_silence, indpb=0.001)