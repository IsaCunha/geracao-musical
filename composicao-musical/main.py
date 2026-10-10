"""
main.py

Ponto de entrada do sistema. Executa o Algoritmo Genético, 
gera o gráfico de evolução e exporta o melhor genótipo para arquivo MIDI.
"""

import os
import random
import numpy as np
import matplotlib.pyplot as plt
from deap import tools

# Importa a configuração evolutiva e o módulo de exportação
from motor_genetico import toolbox
from newMIDI import exportar_para_midi

# ==========================================
# ÁREA DE CONFIGURAÇÃO: HIPERPARÂMETROS
# (Altere estes valores para testar novos resultados)
# ==========================================
POP_SIZE = 75          # Tamanho da população (número de indivíduos)
NGEN = 300             # Número total de gerações
CXPB = 0.2             # Probabilidade de Cruzamento (Crossover)
MUTPB = 0.2            # Probabilidade de Mutação Principal (Alterar nota)
MUTPB_SILENCE = 0.1    # Probabilidade de Mutação de Silêncio (Inserir pausa)
ELITISM_SIZE = 5       # Quantidade de melhores indivíduos mantidos intactos (Elitismo)
# ==========================================
# Nota: Para alterar os instrumentos gerados ou o atraso (cânone), 
# modifique as configurações dentro do arquivo `newMIDI.py`.
# ==========================================

def main():
    pop = toolbox.population(n=POP_SIZE)

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

    # Laço Evolutivo
    for g in range(1, NGEN + 1):

        # Encontra e clona a elite (indivíduos que passam intactos)
        elite = tools.selBest(pop, ELITISM_SIZE)
        elite = list(map(toolbox.clone, elite))

        # Seleciona e clona o restante para reprodução
        offspring = toolbox.select(pop, len(pop) - ELITISM_SIZE)
        offspring = list(map(toolbox.clone, offspring))

        # Aplica o Cruzamento (Crossover)
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Aplica as Mutações
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
                
            if random.random() < MUTPB_SILENCE:
                toolbox.mut_silence(mutant)
                del mutant.fitness.values

        # Recalcula o fitness apenas dos indivíduos que foram modificados
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Atualiza a população com a elite + filhos
        pop[:] = elite + offspring

        # Atualiza e imprime as estatísticas
        record = stats.compile(pop)
        logbook.record(gen=g, **record)
        print(logbook.stream)

    # ==========================================
    # GERAÇÃO DO GRÁFICO E EXPORTAÇÃO
    # ==========================================
    gen = logbook.select("gen")
    fit_max = logbook.select("max")
    fit_avg = logbook.select("avg")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(gen, fit_max, label="Fitness Máximo", color="blue")
    ax.plot(gen, fit_avg, label="Fitness Médio", color="orange")
    
    ax.set_xlabel("Gerações")
    ax.set_ylabel("Fitness (1 / Distância NCD + Penalidades)")
    ax.set_title("Evolução do Algoritmo Genético")
    
    # Monta a caixa de texto usando as variáveis globais que definimos no topo
    texto_parametros = (
        f"População: {POP_SIZE}\n"
        f"Gerações: {NGEN}\n"
        f"Cruzamento (CXPB): {CXPB}\n"
        f"Mut. Notas (MUTPB): {MUTPB}\n"
        f"Mut. Silêncio (SILENCE): {MUTPB_SILENCE}\n"
        f"Elitismo: {ELITISM_SIZE}"
    )
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray')
    ax.text(0.75, 0.40, texto_parametros, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='left', bbox=props)

    ax.legend(loc="lower right")
    plt.grid(True)
    
    # Procura o próximo número disponível para não sobrescrever arquivos
    contador = 1
    nome_grafico = f"Resultados/grafico_evolucao{contador}.png"
    
    # Garante que a pasta Resultados exista
    os.makedirs("Resultados", exist_ok=True)
    
    while os.path.exists(nome_grafico):
        contador += 1
        nome_grafico = f"Resultados/grafico_evolucao{contador}.png"
        
    plt.savefig(nome_grafico, dpi=300, bbox_inches='tight')
    print(f"\nGráfico salvo como: {nome_grafico}")
    
    plt.close()

    # Retorna a população final, o melhor indivíduo e o contador de arquivo
    melhor_individuo = tools.selBest(pop, 1)[0]
    return pop, melhor_individuo, contador


if __name__ == "__main__":
    print("Iniciando composição algorítmica...\n")
    populacao_final, melhor_array, numero_teste = main()
    
    nome_midi = f"Resultados/melodia_natal{numero_teste}.mid"
    exportar_para_midi(melhor_array, nome_midi)
    
    print("\n====================================")
    print("MÚSICA GERADA COM SUCESSO!")
    print(f"Arquivo de áudio salvo em: {nome_midi}")
    print("Melhor genótipo encontrado:")
    print(melhor_array)
    print("====================================")