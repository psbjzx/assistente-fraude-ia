# 6. Pitch de aproximadamente três minutos

Imagine abrir um projeto de detecção de fraude e ver 99,8% de acurácia. Parece ótimo. Mas, nesta base, um sistema que chamasse todas as operações de normais teria praticamente a mesma acurácia e não encontraria nenhuma fraude. Para quem está começando, esse tipo de resultado pode levar à interpretação errada do projeto.

Foi para resolver essa dificuldade que criei o **Lupa**, um assistente de estudo para o case de fraude em cartão de crédito. Ele responde perguntas sobre a base, sobre as métricas que importam, sobre os três modelos testados e sobre a explicação SHAP. Por exemplo: se alguém perguntar “Quantas fraudes o XGBoost encontrou?”, o Lupa informa que foram 85 das 98 fraudes do teste, explica o recall de 86,73% e mostra a seção da fonte interna onde esse número foi registrado.

O funcionamento é simples. Organizei os resultados executados do case em 13 verbetes com respostas revisadas e referências. A aplicação recebe a pergunta e usa processamento de texto com TF-IDF, complementado por sinais de domínio, para localizar o assunto mais adequado. Ela apresenta somente a resposta aprovada daquele verbete, acompanhada de um próximo passo para estudar. Uma interface em Streamlit permite conversar pelo navegador; também existe um modo de terminal. Não é preciso chave de API.

Uma decisão central foi permitir que o assistente diga “não sei”. Se alguém perguntar a cotação do dólar, pedir a identificação de um cliente ou solicitar o bloqueio de uma compra específica, ele informa que esses dados não estão disponíveis. Isso é importante porque o case usa transações históricas anonimizadas, sem acesso a operações bancárias reais. O Lupa é educacional, não uma ferramenta de decisão operacional.

Também registrei uma avaliação que qualquer pessoa pode repetir. Existem 74 perguntas documentadas: 52 cobertas pela base e 22 que devem receber abstenção. A versão atual passa nos casos incluídos e mostra a origem de cada resposta. Isso não significa que ela tenha a mesma qualidade diante de perguntas inéditas: os exemplos foram usados para melhorar o próprio protótipo. O próximo passo é pedir a outras pessoas que façam perguntas novas e revisar a qualidade de cada resposta.

O valor deste projeto está em tornar um resultado técnico compreensível e verificável. A pessoa não recebe apenas um número: entende o que ele mede, onde foi obtido e quando não deve ser usado para tomar uma decisão real.
