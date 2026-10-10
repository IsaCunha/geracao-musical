"""
fitness.py

Implementa a função de avaliação do Algoritmo Genético.
Combina a métrica de Distância de Compressão Normalizada (NCD)
com heurísticas de penalização baseadas em teoria musical básica.
"""

import zlib

def calcular_ncd(array_x, array_y):
    """
    Calcula a Distância de Compressão Normalizada (NCD) entre dois vetores.
    """
    # Converte as listas de inteiros em arrays de bytes
    bytes_x = bytes(array_x)
    bytes_y = bytes(array_y)
    
    # Concatena os dois arrays de bytes (o xy da fórmula)
    bytes_xy = bytes_x + bytes_y 
    
    # Comprime tudo e pega os tamanhos (C(x), C(y) e C(xy))
    c_x = len(zlib.compress(bytes_x))
    c_y = len(zlib.compress(bytes_y))
    c_xy = len(zlib.compress(bytes_xy))
    
    # Aplica a fórmula NCD (corrigida com o sinal de subtração)
    ncd = (c_xy - min(c_x, c_y)) / max(c_x, c_y)
    
    return ncd


def calcular_fitness(genotipo_gerado, lista_de_guias):
    """
    Avalia o indivíduo pela similaridade estrutural com os guias (NCD)
    e aplica penalidades para saltos abruptos e buracos rítmicos.
    """
    soma_distancias = 0
    
    for guia in lista_de_guias:
        distancia = calcular_ncd(genotipo_gerado, guia)
        soma_distancias += distancia

    penalidade_saltos = 0
    
    for i in range(1, len(genotipo_gerado)):
        nota_atual = genotipo_gerado[i]
        nota_anterior = genotipo_gerado[i-1]

        # Punição severa para buracos de silêncio (0 seguido de 0 ou 1)
        if nota_anterior == 0 and (nota_atual == 0 or nota_atual == 1):
            penalidade_saltos += 2.0
            continue
        
        # Ignora os silêncios (0) e legatos (1) no cálculo do salto de altura
        if nota_atual > 1 and nota_anterior > 1:
            distancia_tons = abs(nota_atual - nota_anterior)
            
            # Melodias infantis e natalinas raramente saltam mais que 7 semitons
            if distancia_tons > 7:
                # Quanto maior o salto, maior a penalidade
                penalidade_saltos += (distancia_tons * 0.08)

    # Conta o total de pausas na melodia gerada
    total_silencios = genotipo_gerado.count(0)
    
    # Restrição rígida: máximo de 7 silêncios tolerados
    if total_silencios > 7:
        excesso = total_silencios - 7
        # Multiplicador alto (1.0) garante que a nota despenque no torneio
        penalidade_saltos += (excesso * 1.0)
        
    # Retorna o inverso da soma para que o maior valor seja o melhor fitness
    # Somamos um valor bem pequeno (1e-6) para evitar divisão por zero
    pontuacao_base = soma_distancias + penalidade_saltos
    fitness = 1 / (pontuacao_base + 1e-6)
    
    return fitness