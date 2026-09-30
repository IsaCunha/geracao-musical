Inicialmente, foram selecionadas 7 arquivos MIDI com temática natalina. Todos os arquivos possuíam exatemente dois instrumentos, sendo o primeiro com a melodia e o segundo com a base do piano. Como esse trabalho pretende usar arquivos monofonicos, avaliamos cada um dos audios selecionados inicialmente e medimos seu tamanho (contagem de notas) e polifonia (quantidade de notas sobrepostas). Permaneceram no dataset apenas as melodias sem qualquer polifonia. Isto é: Petit Papa Noel, Jingle Bells, Joy to the World e O Holy Night.


**Tabela 1: Resumo das análises de polifonia**

| Arquivo (.mid) | Inst 0: Notas | Inst 0: Sobrepostas | Inst 0: Polifonia | Inst 1: Notas | Inst 1: Sobrepostas | Inst 1: Polifonia |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| Deck_The_Halls | 1014 | 488 | 48,1% | 637 | 276 | 43,3% | 
| Jingle_Bells | 98 | 0 | 0,0% | 65 | 27 | 41,5% | 
| Joy_to_the_World | 55 | 0 | 0,0% | 22 | 4 | 18,2% | 
| O_Christmas_Tree | 650 | 334 | 51,4% | 357 | 62 | 17,4% | 
| O_Holy_Night | 102 | 0 | 0,0% | 29 | 7 | 10,3% | 
| Petit_Papa_Noel |	124 | 0	| 0,0% | 35 | 0 | 0,0% | 
| We_Wish_You... | 427 | 216 | 50,6% | 192 | 19 | 9,9% | 

