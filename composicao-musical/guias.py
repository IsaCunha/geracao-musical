"""
guias.py

Carrega automaticamente os arquivos MIDI da pasta alvo, extrai os genótipos
usando o extrator_genotipo e disponibiliza o conjunto de guias para a função de fitness.
"""

import os
from extrator_genotipo import extrair_genotipo_quantizado

DIRETORIO_MIDIS = 'Natalinas'
conjunto_guias = []

# 1. Carrega automaticamente a melodia principal (Instrumento 0) de todos os MIDIs
for arquivo in os.listdir(DIRETORIO_MIDIS):
    if arquivo.endswith('.mid'):
        caminho_completo = os.path.join(DIRETORIO_MIDIS, arquivo)
        
        # Extrai o genótipo da melodia
        genotipo, _ = extrair_genotipo_quantizado(caminho_completo, indice_instrumento=0)
        conjunto_guias.append(genotipo)
        
# 2. Adiciona a heurística especial: Instrumento 1 de O Holy Night (Arpejos)
caminho_holy_night = os.path.join(DIRETORIO_MIDIS, 'O_Holy_Night.mid')
if os.path.exists(caminho_holy_night):
    o_holy_down, _ = extrair_genotipo_quantizado(caminho_holy_night, indice_instrumento=1)
    
    # Reduzimos o tamanho da amostra (pegando apenas os primeiros compassos) 
    # para que este acompanhamento não domine a métrica de NCD e cause overfitting.
    conjunto_guias.append(o_holy_down[:90])

print(f"[guias.py] {len(conjunto_guias)} guias carregadas com sucesso da pasta '{DIRETORIO_MIDIS}'.")