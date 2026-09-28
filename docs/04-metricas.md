# 5. Avaliação e métricas

## O que foi medido

Os arquivos `evaluation/questions.json` (34 casos), `evaluation/holdout.json` (20) e `evaluation/challenge.json` (20) declaram a pergunta, a classe esperada (`answered` ou `abstained`) e, quando há resposta, o ID do verbete esperado. `evaluation/evaluate.py` confere:

1. **Roteamento de perguntas cobertas:** resposta encontrada e ID igual ao rotulado.
2. **Abstenção para perguntas sem base:** resposta `abstained` quando o rótulo assim exige.
3. **Fonte visível:** respostas emitidas contêm o ID e o caminho do verbete que foram selecionados.

Uma resposta com o ID certo **não equivale** a um julgamento humano da clareza ou da verdade de toda frase. A verificação de fonte também confirma presença de referência, não uma prova independente de fidelidade semântica.

## Resultado reproduzível da versão entregue

| Roteiro | Roteamento coberto | Abstenção esperada | Respostas com fonte |
| --- | ---: | ---: | ---: |
| `questions.json` | 26/26 | 8/8 | 26/26 |
| `holdout.json` | 13/13 | 7/7 | 13/13 |
| `challenge.json` | 13/13 | 7/7 | 13/13 |
| **Total dos casos documentados** | **52/52** | **22/22** | **52/52** |

Esses três conjuntos foram **usados durante a construção para detectar e corrigir erros**; apesar dos nomes históricos `holdout` e `challenge`, **não são amostras independentes da versão final**. Antes dos ajustes, a segunda bateria teve só **3/13 roteamentos** e **3/7 abstenções** corretos. Essa falha motivou a inclusão de sinônimos, sinais de intenção e verificações explícitas de dados ausentes. Os números finais medem regressões conhecidas, sem estimar desempenho em conversas novas.

Os resultados item a item estão em `evaluation/results_questions.json`, `evaluation/results_holdout.json` e `evaluation/results_challenge.json`. Para reproduzir, execute os três comandos no README; o programa imprime os erros e reescreve os resultados.

Também foi executado `python -m evaluation.smoke_ui`: a interface respondeu uma pergunta coberta com fonte e se absteve diante de uma compra específica, sem erros no aplicativo.

## Revisão qualitativa e riscos remanescentes

Foi conferido manualmente que os textos dos verbetes com números coincidem com `data/fontes-do-case.md`: 492 fraudes, 85/98 detectadas no teste, 77 falsos alertas, limiar 0,189879 e contribuições SHAP na escala correta. A fonte pública identifica a origem dos dados, enquanto a fonte interna registra as métricas daquela execução. Não houve avaliação com pessoas externas, cálculos sobre transações novas ou auditoria de todas as possíveis paráfrases.

**Próxima medição recomendada:** coletar perguntas de pessoas que não participaram do projeto; rotulá-las antes de executar o motor; medir separadamente roteamento, abstenção excessiva, falsas respostas e adequação da explicação por revisão humana. Ajustes nesses exemplos exigiriam outro conjunto não usado no desenvolvimento.
