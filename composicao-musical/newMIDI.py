import pretty_midi

def exportar_para_midi(genotipo, nome_ficheiro="primeira_geracao.mid"):
    # Inicia um ficheiro MIDI em branco
    midi_novo = pretty_midi.PrettyMIDI()

    # Cria um instrumento de Piano Acústico (Programa 0 no padrão General MIDI)
    #piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    #piano = pretty_midi.Instrument(program=piano_program)
    #piano_eletrico = pretty_midi.Instrument(program=4)
    #caixa_musica = pretty_midi.Instrument(program=10) # favorita!!
    #xilofone = pretty_midi.Instrument(program=13)
    #celesta = pretty_midi.Instrument(program=9)
    instrumento = pretty_midi.Instrument(program=10)

    tempo_atual = 0.0
    duracao_nota = 0.50  # Duração fixa de cada semicolcheia (0.25 segundos)

    for valor in genotipo:
        if valor != 0:  # Ignora o silêncio para não criar um evento sonoro
            nota = pretty_midi.Note(
                velocity=100,  # Volume (0 a 127)
                pitch=valor,   # Altura da nota MIDI
                start=tempo_atual,
                end=tempo_atual + duracao_nota
            )
            instrumento.notes.append(nota)
        
        # O ponteiro de tempo avança sempre, independentemente de haver nota ou silêncio
        tempo_atual += duracao_nota

    # Adiciona a faixa ao MIDI e exporta
    midi_novo.instruments.append(instrumento)
    midi_novo.write(nome_ficheiro)
    print(f"\nFicheiro simbólico exportado com sucesso: {nome_ficheiro}")