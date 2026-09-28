# Fonte interna: estudo de detecção de fraude

Este arquivo reúne os fatos usados pelo protótipo. Foram extraídos da execução do projeto **fraude-cartao-credito** nesta sessão (notebook e README, semente aleatória 42). É uma base de demonstração fixa: editar o projeto de origem depois exige revisar esta cópia e reexecutar a avaliação.

## Dados

O conjunto público Credit Card Fraud Detection, associado à ULB/Worldline, tem 284.807 linhas: 284.315 normais e 492 fraudes (0,1727%). Fonte externa: [tutorial do TensorFlow](https://www.tensorflow.org/tutorials/structured_data/imbalanced_data), que carrega [este CSV por URL](https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv). A base original também está no [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud). Consulta da documentação: 27/09/2026.

## Acurácia

Uma regra que classifica tudo como normal acerta 99,8273% das transações e tem recall 0% entre as fraudes. Recall, precisão e F1 da classe 1 descrevem melhor a utilidade de um alerta.

## Preparação

Campos originais: `Time`, `Amount`, `Class`, `V1` a `V28`. As `V` são componentes PCA anonimizadas. Foram criados `LogAmount=log1p(Amount)`, `TimeSin` e `TimeCos` referentes a ciclos de 24 h desde o começo da coleta; não são necessariamente a hora civil. Treino, validação e teste foram separados com estratificação, com 170.883/56.962/56.962 observações e 295/99/98 fraudes, respectivamente. O `StandardScaler` foi ajustado apenas no treino de cada pipeline.

## Treino

Modelos principais: regressão logística com `class_weight=balanced`, Random Forest com `class_weight=balanced_subsample` e XGBoost com `scale_pos_weight≈578,26` (normais/fraudes do treino). Foram comparadas ainda regressões logísticas com undersampling dos normais e oversampling por duplicação de fraudes. Só o treino foi reamostrado.

## Limiar

Para cada modelo, a validação determinou o limiar que maximizava recall sujeito a precisão de pelo menos 50%; empatando, preferia-se maior precisão. O XGBoost foi escolhido na validação, com recall 82,83%, precisão 56,16% e limiar 0,189879. Os 50% são uma escolha didática, não otimizada por custo real. O teste não participou da seleção.

## Modelos

No teste, XGBoost e Random Forest tiveram recall de 86,73%; precisões de 52,47% e 55,56%, respectivamente. A escolha pelo XGBoost foi mantida porque já havia sido feita na validação. A logística ponderada alcançou recall 84,69% e precisão 58,04%; o undersampling alcançou 84,69% e 47,43%; o oversampling, 86,73% e 52,15%.

## Teste

No conjunto de teste, o XGBoost selecionado encontrou 85 das 98 fraudes (TP=85, FN=13); produziu 77 falsos alertas (FP=77) e 56.787 normais corretamente ignoradas (TN=56.787). Recall 86,73%; precisão 52,47%; F1 65,38%; ROC-AUC 0,9774; AP ou PR-AUC 0,8629. Os pesos da matriz de confusão referem-se ao limiar 0,189879.

## Explicação

Na transação com índice original 77348 (classe real 1, alerta 1), a pontuação foi 0,999899. No gráfico SHAP local do XGBoost, V14 (+3,493), V12 (+1,554) e V10 (+1,504) aumentaram a pontuação; V8 (−0,795) a diminuiu. Os valores SHAP estão em log-odds. Componentes PCA não permitem atribuir uma causa ou comportamento de cliente a essas variáveis.

## Limites

A base histórica tem poucas fraudes. A divisão foi aleatória e estratificada; uma avaliação temporal ajudaria a estimar desempenho futuro. Não há identificador de cliente para histórico individual. Pesos e reamostragem podem afetar calibração. Não existem custos operacionais informados e a experiência não justifica bloquear pagamentos reais.
