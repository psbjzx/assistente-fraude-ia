"""NLP local: busca TF-IDF e respostas aprovadas da base de conhecimento.

Sem LLM generativo. Nenhum texto factual é redigido dinamicamente; o
algoritmo seleciona uma resposta revisada e inclui a fonte correspondente.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
import unicodedata

from sklearn.feature_extraction.text import TfidfVectorizer


ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Reply:
    status: str
    text: str
    article_id: str | None = None
    title: str | None = None
    source: str | None = None
    score: float | None = None


def _plain(text: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', text.lower())
                   if not unicodedata.combining(c))


class FraudCaseAssistant:
    """Seleciona a melhor pergunta exemplificativa e pode se abster."""

    def __init__(self, root: Path = ROOT, min_score: float = 0.22,
                 ambiguity_margin: float = 0.025):
        self.root = Path(root)
        self.articles = json.loads((self.root / 'data/knowledge.json').read_text(encoding='utf-8'))
        self.policy = json.loads((self.root / 'data/response_policy.json').read_text(encoding='utf-8'))
        self.intent_signals = json.loads((self.root / 'data/intent_signals.json').read_text(encoding='utf-8'))
        ids = [item['id'] for item in self.articles]
        if len(ids) != len(set(ids)):
            raise ValueError('Os identificadores da base devem ser únicos.')
        if not all((self.root / item['source'].split('#', 1)[0]).is_file()
                   for item in self.articles):
            raise ValueError('Há uma referência de fonte sem arquivo no projeto.')

        self.min_score = min_score
        self.ambiguity_margin = ambiguity_margin
        self.examples = [(item['id'], question)
                         for item in self.articles
                         for question in item['questions'] + item.get('aliases', [])]
        questions = [question for _, question in self.examples]
        self.word = TfidfVectorizer(strip_accents='unicode', ngram_range=(1, 2),
                                    sublinear_tf=True)
        self.char = TfidfVectorizer(strip_accents='unicode', analyzer='char_wb',
                                    ngram_range=(3, 5), sublinear_tf=True)
        self.word_matrix = self.word.fit_transform(questions)
        self.char_matrix = self.char.fit_transform(questions)

    def _rank(self, query: str) -> list[tuple[str, float]]:
        # TF-IDF já usa norma L2; o produto escalar dá similaridade cosseno.
        word_scores = (self.word.transform([query]) @ self.word_matrix.T).toarray().ravel()
        char_scores = (self.char.transform([query]) @ self.char_matrix.T).toarray().ravel()
        combined = 0.78 * word_scores + 0.22 * char_scores
        by_article: dict[str, float] = {}
        for (article_id, _), score in zip(self.examples, combined):
            by_article[article_id] = max(by_article.get(article_id, 0.0), float(score))
        normalized = _plain(query)
        for article_id, rules in self.intent_signals.items():
            bonus = min(0.70, sum(weight for pattern, weight in rules
                                  if re.search(pattern, normalized)))
            by_article[article_id] += bonus
        return sorted(by_article.items(), key=lambda row: row[1], reverse=True)

    def ask(self, query: str) -> Reply:
        query = query.strip()
        if not query:
            return Reply('abstained', self.policy['empty'])
        if len(query) > 500:
            return Reply('abstained', self.policy['too_long'])

        normalized = _plain(query)
        if re.search(r'(ignore|desconsidere|revele|mostre).{0,45}'
                     r'(instruc|prompt|regras|politica)', normalized):
            return Reply('abstained', self.policy['instruction_override'])
        # Informações que a base não contém, mesmo quando a pergunta menciona
        # uma métrica ou um número do case.
        if re.search(r'\b(svm|cotacao|dolar|saldo|conta bancaria|loja|'
                     r'estabelecimento|titular)\b|previsao do tempo|'
                     r'(valor|custo|perda) total.{0,25}(fraude|reais|perdido)', normalized):
            return Reply('abstained', self.policy['unknown'])
        if re.search(r'\b(taxa de juros|banco emissor|id do cliente|'
                     r'identificador do cliente|cpf|senhas?|endereco do cliente)\b', normalized):
            return Reply('abstained', self.policy['unknown'])
        if re.search(r'\b(tenho|tive|fiz|recebi|paguei|devo)\b.{0,50}'
                     r'\b(transacao|compra|cartao|pagamento)\b', normalized):
            return Reply('abstained', self.policy['specific_transaction'])
        years = re.findall(r'\b(?:19\d{2}|20\d{2})\b', normalized)
        if any(year != '2013' for year in years):
            return Reply('abstained', self.policy['unknown'])
        if re.search(r'\b(minha|meu|essa|esta)\b.{0,45}'
                     r'\b(compra|transacao|cartao|pagamento)\b', normalized) \
                or re.search(r'\b(compra|transacao|cartao|pagamento)\b.{0,45}'
                             r'\b(minha|meu|essa|esta)\b', normalized):
            return Reply('abstained', self.policy['specific_transaction'])

        ranking = self._rank(query)
        article_id, score = ranking[0]
        if score < self.min_score:
            return Reply('abstained', self.policy['unknown'], score=score)
        second_id, second_score = ranking[1]
        if score - second_score < self.ambiguity_margin:
            return Reply('clarify', self.policy['ambiguous'], score=score)

        article = next(item for item in self.articles if item['id'] == article_id)
        text = (f"{article['answer']}\n\n"
                f"**{self.policy['next_step_label']}:** {article['next_step']}\n\n"
                f"**{self.policy['source_label']}:** [{article['id']}] "
                f"{article['source']}")
        return Reply('answered', text, article_id=article_id,
                     title=article['title'], source=article['source'], score=score)


def main() -> None:
    agent = FraudCaseAssistant()
    print('Lupa — tutor do case de fraude. Pergunte sobre dados, modelos ou métricas.')
    print('Digite sair para encerrar.\n')
    while True:
        try:
            question = input('Você: ')
        except (EOFError, KeyboardInterrupt):
            print('\nAté logo.')
            break
        if _plain(question.strip()) in {'sair', 'exit', 'quit'}:
            print('Até logo.')
            break
        reply = agent.ask(question)
        print(f'\nLupa: {reply.text}\n')


if __name__ == '__main__':
    main()
