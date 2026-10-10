"""
motor_genetico.py

Configuração do Algoritmo Genético usando a biblioteca DEAP.
Define a representação do indivíduo, população e os operadores evolutivos 
(cruzamento, mutação, seleção e avaliação).
"""

import random
from deap import base, creator, tools

# Importações dos módulos locais
from fitness import calcular_fitness
from guias import conjunto_guias

# ==========================================
# 1. Configuração Base do DEAP
# ==========================================
# O objetivo é maximizar o fitness (por isso weights=(1.0,))
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# ==========================================
# 2. Representação do Genótipo
# ==========================================
# Tamanho do indivíduo: 128 ticks de 0.25s = 32 segundos de música
IND_SIZE = 128

# Notas restritas à escala de Dó Maior (C Major), mais o token de legato (1). 
# Os silêncios (0) não nascem na geração inicial, são inseridos via mutação.
ESCALA_MAIOR = [1, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79]

def gerar_nota():
    """Gera um gene inicial aleatório baseado na escala permitida."""
    return random.choice(ESCALA_MAIOR)

toolbox.register("attribute", gerar_nota)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# ==========================================
# 3. Definição dos Operadores
# ==========================================
def evaluate(individuo):
    """Calcula o fitness do indivíduo usando a NCD e penalidades."""
    # O DEAP exige que a função de fitness retorne uma tupla
    fitness_ind = calcular_fitness(individuo, conjunto_guias)
    return (fitness_ind,)

def mut_escala(individual, indpb):
    """Mutação principal: altera uma nota existente para outra da escala."""
    for i in range(len(individual)):
        if random.random() < indpb and individual[i] != 0:
            individual[i] = random.choice(ESCALA_MAIOR)
    return (individual,)

def mut_silence(individual, indpb):
    """Mutação de silêncio: insere pausas (0) aleatoriamente na melodia."""
    for i in range(len(individual)):
        if random.random() < indpb and individual[i] != 0:
            individual[i] = 0
    return (individual,)

# ==========================================
# 4. Registro na Toolbox
# ==========================================
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)                      # Cruzamento de 2 pontos
toolbox.register("select", tools.selTournament, tournsize=10)   # Torneio
toolbox.register("mutate", mut_escala, indpb=0.05)              # Mutação principal
toolbox.register("mut_silence", mut_silence, indpb=0.001)       # Mutação de pausas