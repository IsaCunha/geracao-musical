import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools
from algorithm import *
from newMIDI import exportar_para_midi
# Supondo que as definições do seu toolbox estejam aqui em cima

def main():
    pop = toolbox.population(n=50)
    CXPB, MUTPB, MUTPB_SILENCE, NGEN = 0.2, 0.2, 0, 2000

    # Configuração da captura de estatísticas
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("max", np.max)
    
    # O Logbook vai guardar os dados de cada geração
    logbook = tools.Logbook()
    logbook.header = "gen", "avg", "max"

    # Avalia a população inicial
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Grava as estatísticas da geração 0
    record = stats.compile(pop)
    logbook.record(gen=0, **record)
    print(logbook.stream)

    for g in range(1, NGEN + 1):

        # Encontra e clona o melhor indivíduo da geração atual (O Elite)
        elite = tools.selBest(pop, 1)
        elite = list(map(toolbox.clone, elite))

        # Seleciona, clona e aplica cruzamento/mutação
        offspring = toolbox.select(pop, len(pop)-1)
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            # Mutação tradicional (altera a nota)
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
                
            # Mutação de silêncio (insere 0)
            if random.random() < MUTPB_SILENCE:
                toolbox.mut_silence(mutant)
                del mutant.fitness.values

        # Recalcula o fitness apenas dos indivíduos modificados
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = elite + offspring

        # Atualiza e imprime as estatísticas da geração atual
        record = stats.compile(pop)
        logbook.record(gen=g, **record)
        print(logbook.stream)

   # Extrai os dados do logbook para plotar
    gen = logbook.select("gen")
    fit_max = logbook.select("max")
    fit_avg = logbook.select("avg")

    # Gera o gráfico de evolução do fitness
    fig, ax = plt.subplots(figsize=(8, 6)) # Aumentei um pouco a figura para caber tudo confortavelmente
    ax.plot(gen, fit_max, label="Fitness Máximo", color="blue")
    ax.plot(gen, fit_avg, label="Fitness Médio", color="orange")
    
    ax.set_xlabel("Gerações")
    ax.set_ylabel("Fitness (1 / Distância NCD)")
    ax.set_title("Evolução do Algoritmo Genético")
    
    # Texto com os hiperparâmetros para anotação
    texto_parametros = (
        f"População: {len(pop)}\n"
        f"Gerações: {NGEN}\n"
        f"Cruzamento (CXPB): {CXPB}\n"
        f"Mut. Notas (MUTPB): {MUTPB}\n"
        f"Mut. Silêncio (SILENCE): {MUTPB_SILENCE}\n"
        f"Torneio: 10"
    )
    
    # Desenha a caixa de texto no canto inferior direito (coordenadas relativas de 0 a 1)
    props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray')
    ax.text(0.75, 0.40, texto_parametros, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='left', bbox=props)

    ax.legend(loc="lower right")
    plt.grid(True)
    plt.show()

    # Retorna a população final e o melhor indivíduo encontrado
    melhor_individuo = tools.selBest(pop, 1)[0]
    return pop, melhor_individuo

if __name__ == "__main__":
    populacao_final, melhor_array = main()
    exportar_para_midi(melhor_array, "melodia_natal_piano.mid")
    print("Melhor genótipo encontrado:", melhor_array)