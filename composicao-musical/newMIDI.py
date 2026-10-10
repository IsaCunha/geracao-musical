"""
newMIDI.py

Responsável por converter o genótipo evoluído (vetor numérico) em um arquivo de áudio MIDI.
Aplica técnicas de layering (camadas de instrumentos) e cânone (atraso/eco) 
para enriquecer a textura musical das melodias natalinas.
"""

import pretty_midi
import copy

def exportar_para_midi(genotipo, nome_ficheiro="melodia_gerada.mid"):
    # =================================================================
    # ÁREA DE CONFIGURAÇÃO DE TIMBRES E EFEITOS
    # Altere os valores abaixo para testar novas sonoridades!
    # =================================================================
    # Combinações natalinas testadas com sucesso:
    # 1. Piano (0) + Flute (73), atraso = 0
    # 2. Celesta (9) + Choir Aahs (52), atraso = 2
    # 3. Music Box (10) + Piano (0), atraso = 0
    # 4. Xilofone (13), Eletric Piano (4).
    # =================================================================
    PROGRAMA_PRINCIPAL = 13       # Instrumento principal (ex: 9 = Celesta)
    PROGRAMA_SECUNDARIO = 4     # Instrumento de fundo (ex: 52 = Coral)
    
    ATRASO_EM_NOTAS = 1          # Quantidade de 'ticks' de atraso (0 para uníssono)
    VELOCIDADE_ECO = 70          # Volume do instrumento secundário (0 a 127)
    TEMPO_BASE = 0.25            # Resolução temporal da grade (0.25s por token)
    # =================================================================

    # Inicia um ficheiro MIDI em branco
    midi_novo = pretty_midi.PrettyMIDI()

    # Cria as instâncias dos instrumentos
    instrumento_principal = pretty_midi.Instrument(program=PROGRAMA_PRINCIPAL)
    instrumento_secundario = pretty_midi.Instrument(program=PROGRAMA_SECUNDARIO)

    tempo_atual = 0.0
    nota_em_execucao = None
    inicio_nota = 0.0

    # Percorre o DNA da música
    for valor in genotipo:
        if valor == 0: 
           # Silêncio: corta a nota atual e grava no arquivo
            if nota_em_execucao is not None:
                nota_midi = pretty_midi.Note(
                    velocity=100, pitch=nota_em_execucao,
                    start=inicio_nota, end=tempo_atual
                )
                instrumento_principal.notes.append(nota_midi)
                nota_em_execucao = None

        elif valor == 1:
            # Sustentação (Legato): Não fazemos nada. 
            # O tempo avança, efetivamente "esticando" a nota que já está tocando.
            pass

        else:
            # É uma nota nova (ex: 60, 62...)
            # Se já havia uma nota tocando, corta e grava ela antes de começar a nova
            if nota_em_execucao is not None:
                nota_midi = pretty_midi.Note(
                    velocity=100, pitch=nota_em_execucao,
                    start=inicio_nota, end=tempo_atual
                )
                instrumento_principal.notes.append(nota_midi)
            
            # Atualiza a memória com a nova nota
            nota_em_execucao = valor
            inicio_nota = tempo_atual
            
        # O ponteiro de tempo SEMPRE avança a cada token lido
        tempo_atual += TEMPO_BASE

    # Garante que a última nota do vetor não seja perdida ao final do loop
    if nota_em_execucao is not None:
        nota_midi = pretty_midi.Note(
            velocity=100, pitch=nota_em_execucao,
            start=inicio_nota, end=tempo_atual
        )
        instrumento_principal.notes.append(nota_midi)


    # =================================================================
    # EFEITO DE LAYERING / CÂNONE
    # =================================================================
    # Clona a melodia perfeita do instrumento principal para o secundário
    instrumento_secundario.notes = copy.deepcopy(instrumento_principal.notes)

    # Converte o atraso de notas para segundos (ex: 2 notas * 0.25s = 0.5s de atraso)
    tempo_de_atraso = ATRASO_EM_NOTAS * TEMPO_BASE
    
    for nota in instrumento_secundario.notes:
        # Empurra a nota para o futuro
        nota.start += tempo_de_atraso
        nota.end += tempo_de_atraso
        
        # Reduz o volume para criar profundidade sonora
        nota.velocity = VELOCIDADE_ECO

    # Adiciona as duas faixas ao arquivo principal e salva
    midi_novo.instruments.append(instrumento_principal)
    midi_novo.instruments.append(instrumento_secundario)
    
    midi_novo.write(nome_ficheiro)