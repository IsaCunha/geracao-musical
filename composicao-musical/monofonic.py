import pretty_midi

midi_data = pretty_midi.PrettyMIDI('Natalinas/Jingle_Bells.mid')

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

array_genotipo = []

# Itera sobre todas as notas desse instrumento cronologicamente
for nota in melodia.notes:
    array_genotipo.append(nota.pitch)

print(f"Genótipo extraído ({len(array_genotipo)} notas):")
print(array_genotipo)