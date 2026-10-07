import pretty_midi

midi_data = pretty_midi.PrettyMIDI('Natalinas/Petit_Papa_Noel.mid')

def verificar_monofonia(instrumento):
    notas_ordenadas = sorted(instrumento.notes, key=lambda x: x.start)
    sobreposicoes = 0
    
    for i in range(len(notas_ordenadas) - 1):
        # Se a nota atual terminar DEPOIS que a próxima começar, há sobreposição (polifonia)
        if notas_ordenadas[i].end > notas_ordenadas[i+1].start + 0.01: # margem de 10ms
            sobreposicoes += 1
            
    proporcao = (sobreposicoes / len(instrumento.notes)) * 100 if instrumento.notes else 0
    return sobreposicoes, proporcao

# Passa por cada instrumento encontrado no arquivo MIDI
for i, inst in enumerate(midi_data.instruments):
    sub, prop = verificar_monofonia(inst)

    print(f"\nInstrumento {i}: {inst.name}")
    print(f"Total de notas: {len(inst.notes)}")
    print(f"{sub} notas sobrepostas ({prop:.1f}% de polifonia)")


# Após avaliar os arquivos, foi decidido manter apenas o instrumento 0,
# que possuí a melodia principal.
melodia = midi_data.instruments[0]
notas_ordenadas = sorted(melodia.notes, key=lambda x: x.start)

tempo_base = 0.25

# Descobre o tempo final da música (em segundos) para saber o tamanho da matriz
tempo_final = max([nota.end for nota in notas_ordenadas]) if notas_ordenadas else 0
tamanho_grid = int(round(tempo_final / tempo_base))

# Inicia o genótipo inteiro com silêncios (0)
array_genotipo = [0] * tamanho_grid

for nota in notas_ordenadas:
    # Arredonda o tempo do MIDI para encaixar na nossa grade de 0.25s (Quantização)
    idx_inicio = int(round(nota.start / tempo_base))
    idx_fim = int(round(nota.end / tempo_base))
    
    # Se a nota for muito rápida no MIDI original, garantimos pelo menos 1 'tick' (0.25s)
    if idx_fim <= idx_inicio:
        idx_fim = idx_inicio + 1
        
    # A posição exata de início recebe a altura da nota (ex: 67)
    if idx_inicio < tamanho_grid:
        array_genotipo[idx_inicio] = nota.pitch
        
    # As posições seguintes, até a nota acabar, recebem o token de sustentação (1)
    for i in range(idx_inicio + 1, idx_fim):
        if i < tamanho_grid:
            # Só coloca o '1' se o espaço estiver vazio (isso ignora polifonias residuais)
            if array_genotipo[i] == 0:
                array_genotipo[i] = 1

print(f"Genótipo extraído ({len(array_genotipo)} ticks de {tempo_base}s):")
print(array_genotipo)