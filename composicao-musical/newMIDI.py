import pretty_midi
import copy

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
    instrumento = pretty_midi.Instrument(program=9)
    instrumento2 = pretty_midi.Instrument(program=52)

    #combinações natalinas => (O,73, a=0), (9,52, a=2) (14,60, a=0)

    tempo_atual = 0.0
    tempo_base = 0.50

    nota_em_execucao = None
    inicio_nota = 0.0

    for valor in genotipo:
        if valor == 0: 
           # Silêncio: corta a nota atual e grava no arquivo
            if nota_em_execucao is not None:
                nota_midi = pretty_midi.Note(
                    velocity=100, pitch=nota_em_execucao,
                    start=inicio_nota, end=tempo_atual
                )
                instrumento.notes.append(nota_midi)
                nota_em_execucao = None

        elif valor == 1:
            # Sustentação (Legato): Não fazemos absolutamente nada! 
            # Apenas deixamos o tempo_atual avançar lá embaixo, esticando a nota.
            pass

        else:
            # É uma nota nova (ex: 60, 62...)
            # Corta a nota que estava tocando antes
            if nota_em_execucao is not None:
                nota_midi = pretty_midi.Note(
                    velocity=100, pitch=nota_em_execucao,
                    start=inicio_nota, end=tempo_atual
                )
                instrumento.notes.append(nota_midi)
            
            # Atualiza a memória com a nova nota
            nota_em_execucao = valor
            inicio_nota = tempo_atual
            
        # O ponteiro de tempo SEMPRE avança
        tempo_atual += tempo_base

    # Garante que a última nota do vetor não seja esquecida
    if nota_em_execucao is not None:
        nota_midi = pretty_midi.Note(
            velocity=100, pitch=nota_em_execucao,
            start=inicio_nota, end=tempo_atual
        )
        instrumento.notes.append(nota_midi)


    instrumento2.notes = copy.deepcopy(instrumento.notes)

    atraso_em_notas = 2 # Defina aqui 1 ou 2 notas de atraso
    tempo_de_atraso = atraso_em_notas * tempo_base
    
    for nota in instrumento2.notes:
        # Empurra a nota para o futuro
        nota.start += tempo_de_atraso
        nota.end += tempo_de_atraso
        
        # Reduz o volume do eco para 70 (o principal é 100) para criar profundidade
        nota.velocity = 70

    midi_novo.instruments.append(instrumento)
    midi_novo.instruments.append(instrumento2)
    midi_novo.write(nome_ficheiro)
    print(f"\nFicheiro simbólico exportado com sucesso: {nome_ficheiro}")