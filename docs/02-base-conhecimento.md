# 2. Base de conhecimento

## Origem e atualização

Os 13 verbetes em `data/knowledge.json` resumem a análise executada do projeto de detecção de fraude desenvolvido anteriormente. Os números, as definições e os limites são registrados em `data/fontes-do-case.md`. A origem pública da base de transações é o [tutorial do TensorFlow](https://www.tensorflow.org/tutorials/structured_data/imbalanced_data). O CSV completo não é necessário para o assistente e não é incluído.

As informações descrevem **uma execução fixa do experimento**. Se sementes, divisão, modelos ou limiares forem alterados, deve-se atualizar as respostas e rodar novamente os três roteiros de avaliação.

## Esquema de cada verbete

- `id`: identificador imutável usado em citações e avaliações.
- `title`: nome legível do assunto.
- `questions`: exemplos de pergunta para a busca de texto.
- `aliases`: paráfrases curadas durante o desenvolvimento; não são respostas novas.
- `answer`: resposta revisada, baseada na fonte interna.
- `next_step`: sugestão de leitura ou pergunta seguinte.
- `source`: caminho e seção em `data/fontes-do-case.md`.

## Cobertura

| IDs | Assuntos |
| --- | --- |
| CASE-01 a CASE-03 | Base, acurácia enganosa e recall. |
| CASE-04 a CASE-06 | Precisão, F1 e limiar. |
| CASE-07 a CASE-09 | Comparação de modelos, balanceamento e separação de dados. |
| CASE-10 a CASE-13 | PCA, SHAP, curvas e limites operacionais. |

## Controle de qualidade

Os caminhos de fonte são validados na carga. Toda resposta encontrada inclui o ID de seu verbete. Perguntas sobre clientes, comerciantes, perdas financeiras individuais, cotação atual ou classificação de compras reais ficam fora do conjunto de evidências. A recuperação de uma resposta errada ainda pode ocorrer: o teste de perguntas documentadas reduz regressões conhecidas, e uma revisão independente com usuários reais continua necessária.
