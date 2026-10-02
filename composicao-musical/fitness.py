import zlib
from guias import *

def calcular_ncd(array_x, array_y):
    # Converte as listas de inteiros em arrays de bytes
    bytes_x = bytes(array_x)
    bytes_y = bytes(array_y)
    
    # Concatena os dois arrays de bytes (o xy da fórmula)
    bytes_xy = bytes_x + bytes_y 
    
    # Comprime tudo e pega os tamanhos (C(x), C(y) e C(xy))
    c_x = len(zlib.compress(bytes_x))
    c_y = len(zlib.compress(bytes_y))
    c_xy = len(zlib.compress(bytes_xy))
    
    # Aplica a fórmula NCD
    ncd = (c_xy - min(c_x, c_y)) / max(c_x, c_y)
    return ncd

def calcular_fitness(genotipo_gerado, lista_de_guias):
    soma_distancias = 0
    
    for guia in lista_de_guias:
        distancia = calcular_ncd(genotipo_gerado, guia)
        soma_distancias += distancia

    # Penalidade por saltos entre notas
    penalidade_saltos = 0
    for i in range(1, len(genotipo_gerado)):
        nota_atual = genotipo_gerado[i]
        nota_anterior = genotipo_gerado[i-1]

        # Punição severa para buracos de silêncio (0 seguidos)
        if nota_atual == 0 and nota_anterior == 0:
            penalidade_saltos += 2.0
            continue
        
        # Ignora os silêncios (0) no cálculo do salto
        if nota_atual != 0 and nota_anterior != 0:
            distancia = abs(nota_atual - nota_anterior)
            # Melodias infantis e natalinas raramente saltam mais que 7 semitons
            if distancia > 3:
                # Quanto maior o salto, maior a penalidade
                penalidade_saltos += (distancia * 0.1)

    # Conta o total de pausas na melodia gerada
    total_silencios = genotipo_gerado.count(0)
    
    # Restrição rígida: máximo de 5 silêncios
    if total_silencios > 7:
        excesso = total_silencios - 5
        # Multiplicador alto (ex: 3.0) garante que a nota despenque
        # Um indivíduo com 8 silêncios tomaria 9.0 de penalidade, sendo eliminado no torneio
        penalidade_saltos += (excesso * 3.0)
        
    # Retorna o inverso da soma para que o maior valor seja o melhor fitness
    # Somamos um valor bem pequeno (1e-6) para evitar divisão por zero
    pontuação_base = soma_distancias + penalidade_saltos
    fitness = 1 / (pontuação_base + 1e-6)
    return fitness

