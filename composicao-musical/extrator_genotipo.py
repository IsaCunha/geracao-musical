"""
extrator_genotipo.py

Script responsável por ler arquivos MIDI, verificar a taxa de polifonia
e extrair a melodia principal para uma grade temporal quantizada (genótipo),
utilizando tokens específicos para altura (pitch), silêncio (0) e legato (1).
"""

import pretty_midi

def verificar_monofonia(instrumento):
    """
    Verifica a taxa de polifonia de um instrumento MIDI, calculando 
    a quantidade de notas que se sobrepõem no tempo.
    
    Parâmetros:
        instrumento (pretty_midi.Instrument): O instrumento a ser avaliado.
    Retorna:
        tuple: (quantidade de notas sobrepostas, proporção em porcentagem)
    """
    notas_ordenadas = sorted(instrumento.notes, key=lambda x: x.start)
    sobreposicoes = 0
    
    for i in range(len(notas_ordenadas) - 1):
        # Se a nota atual terminar DEPOIS que a próxima começar, há sobreposição
        # É aplicada uma margem de 10ms (0.01s) para evitar falsos positivos
        if notas_ordenadas[i].end > notas_ordenadas[i+1].start + 0.01:
            sobreposicoes += 1
            
    proporcao = (sobreposicoes / len(instrumento.notes)) * 100 if instrumento.notes else 0
    return sobreposicoes, proporcao


def extrair_genotipo_quantizado(caminho_arquivo, indice_instrumento=0, tempo_base=0.25):
    """
    Lê um arquivo MIDI e converte a melodia em um vetor (array) quantizado.
    
    Parâmetros:
        caminho_arquivo (str): Caminho para o arquivo .mid.
        indice_instrumento (int): Qual instrumento do MIDI utilizar (padrão é 0).
        tempo_base (float): Tamanho de cada célula da grade em segundos (padrão 0.25s).
    Retorna:
        list: Vetor representando o genótipo da música.
    """
    midi_data = pretty_midi.PrettyMIDI(caminho_arquivo)
    
    # Seleciona o instrumento (geralmente o 0 contém a melodia principal)
    melodia = midi_data.instruments[indice_instrumento]
    notas_ordenadas = sorted(melodia.notes, key=lambda x: x.start)

    # Descobre o tempo final da música (em segundos) para dimensionar a matriz
    tempo_final = max([nota.end for nota in notas_ordenadas]) if notas_ordenadas else 0
    tamanho_grid = int(round(tempo_final / tempo_base))

    # Inicializa o genótipo inteiro com silêncios (0)
    array_genotipo = [0] * tamanho_grid

    for nota in notas_ordenadas:
        # Arredonda o tempo do MIDI para encaixar na nossa grade (Quantização)
        idx_inicio = int(round(nota.start / tempo_base))
        idx_fim = int(round(nota.end / tempo_base))
        
        # Se a nota for muito rápida no original, garante pelo menos 1 'tick'
        if idx_fim <= idx_inicio:
            idx_fim = idx_inicio + 1
            
        # A posição exata de início recebe a altura da nota (ex: 67)
        if idx_inicio < tamanho_grid:
            array_genotipo[idx_inicio] = nota.pitch
            
        # As posições seguintes, até a nota acabar, recebem o token de sustentação (1)
        for i in range(idx_inicio + 1, idx_fim):
            if i < tamanho_grid:
                # Só insere o '1' se o espaço estiver vazio (ignora polifonias residuais)
                if array_genotipo[i] == 0:
                    array_genotipo[i] = 1

    return array_genotipo, midi_data


# Bloco de execução principal (só roda se o script for executado diretamente)
if __name__ == "__main__":
    arquivo_alvo = 'Natalinas/Petit_Papa_Noel.mid'
    
    # 1. Análise de Polifonia
    print("--- Análise de Polifonia ---")
    midi_temporario = pretty_midi.PrettyMIDI(arquivo_alvo)
    for i, inst in enumerate(midi_temporario.instruments):
        sub, prop = verificar_monofonia(inst)
        print(f"Instrumento {i}: {inst.name}")
        print(f"  Total de notas: {len(inst.notes)}")
        print(f"  {sub} notas sobrepostas ({prop:.1f}% de polifonia)\n")

    # 2. Extração do Genótipo
    print("--- Extração de Genótipo ---")
    genotipo, _ = extrair_genotipo_quantizado(arquivo_alvo, indice_instrumento=0, tempo_base=0.25)
    
    print(f"Genótipo extraído com sucesso ({len(genotipo)} ticks de 0.25s):")
    print(genotipo)