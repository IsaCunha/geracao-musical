# TP1: Composição Musical Algorítmica com Algoritmos Genéticos

Este projeto gera melodias natalinas originais utilizando Algoritmos Genéticos. O processo evolutivo é guiado por uma função de fitness baseada na Distância de Compressão Normalizada (NCD), que avalia a similaridade estrutural entre as melodias geradas e um conjunto de cantigas natalinas de domínio público.

## Como Executar

1. Certifique-se de ter o Python 3 instalado.
2. Instale as bibliotecas necessárias executando o comando abaixo no terminal:
   ```bash
   pip install -r requirements.txt
3. Entre na pasta do TP1 'composicao-musical'.
4. Execute o script principal para iniciar a evolução e gerar a música:
    ```bash
    python main.py

Os resultados (gráficos de evolução e arquivos de áudio .mid) serão salvos automaticamente na pasta Resultados. Para ouvir os arquivos MIDI com qualidade, recomenda-se importá-los em softwares como o MuseScore ou Players online.

## Parâmetros Customizáveis

O sistema foi desenhado de forma modular. Você pode alterar a sonoridade e o comportamento da evolução modificando as variáveis globais localizadas no topo de dois arquivos:

Em *main.py* (Hiperparâmetros do Algoritmo Genético):
Você pode controlar o tamanho da população (POP_SIZE), limite de gerações (NGEN), taxas de mutação de notas (MUTPB) e pausas (MUTPB_SILENCE), probabilidade de cruzamento (CXPB) e o tamanho do elitismo (ELITISM_SIZE).

Em *newMIDI.py* (Síntese de Áudio):
Você pode alterar os timbres dos instrumentos (via PROGRAMA_PRINCIPAL e PROGRAMA_SECUNDARIO), o tempo base, e ajustar o efeito de cânone (atraso e volume do eco).

## Configurações das Músicas Geradas

As três músicas exportadas como resultado deste trabalho utilizaram as seguintes combinações de hiperparâmetros, demonstrando a versatilidade do modelo:

### Música 1 

    *Genético:* 
    População = 100, 
    Gerações = 500, 
    Cruzamento = 0.2, 
    Mutação (Nota) = 0.2, 
    Mutação (Pausa) = 0.1, 
    Elitismo = 5.

    *Áudio:*
    Principal = 9 (Celesta), 
    Fundo = 52 (Coral), 
    Atraso = 0 tick, 
    Eco = 60, 
    Tempo = 0.50s.

### Música 2 

    *Genético:* 
    População = 50, 
    Gerações = 500, 
    Cruzamento = 0.4, 
    Mutação (Nota) = 0.2, 
    Mutação (Pausa) = 0.2, 
    Elitismo = 5.

    *Áudio:*
    Principal = 9 (Celesta), 
    Fundo = 52 (Coral),
    Atraso = 1 tick, 
    Eco = 50, 
    Tempo = 0.25s.

### Música 3 (exemplo usado no artigo)

    *Genético:*  
    População = 75, 
    Gerações = 300, 
    Cruzamento = 0.4, 
    Mutação (Nota) = 0.4, 
    Mutação (Pausa) = 0.1, 
    Elitismo = 10.

    *Áudio:* 
    Principal = 10 (Caixa de Música), 
    Fundo = 0 (Piano), 
    Atraso = 1 tick, 
    Eco = 70, 
    Tempo = 0.50s.

## Declaração de Uso de IA

Em conformidade com as diretrizes do trabalho e a política do ISMIR 2026, declaro o uso do modelo de linguagem Google Gemini durante o desenvolvimento deste projeto. A ferramenta auxiliou na depuração de código da biblioteca pretty_midi, na modularização dos scripts Python, na formatação estrutural em LaTeX do resumo expandido e na revisão gramatical. O delineamento metodológico e as regras das heurísticas foram criadas por mim. O histórico integral das interações pode ser acessado no link: [[LINK_DO_CHAT](https://share.gemini.google/IrUa0TdwQ5oT)].