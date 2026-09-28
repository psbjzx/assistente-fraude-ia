"""Avaliação de roteamento e abstenção; não mede verdade factual sozinha."""

from __future__ import annotations

from pathlib import Path
import argparse
import json

from src.assistant import FraudCaseAssistant


ROOT = Path(__file__).resolve().parent.parent


def evaluate(dataset: str = 'questions') -> dict:
    items = json.loads((ROOT / f'evaluation/{dataset}.json').read_text(encoding='utf-8'))
    agent = FraudCaseAssistant(root=ROOT)
    rows = []
    for item in items:
        reply = agent.ask(item['question'])
        correct = (reply.status == item['status'] and
                   (item['status'] != 'answered' or reply.article_id == item['article_id']))
        rows.append({
            'id': item['id'], 'question': item['question'],
            'expected_status': item['status'], 'status': reply.status,
            'expected_article': item.get('article_id'), 'article': reply.article_id,
            'score': round(reply.score, 3) if reply.score is not None else None,
            'correct': bool(correct),
            'has_source': (reply.source in reply.text and
                           f"[{reply.article_id}]" in reply.text) if reply.status == 'answered' else None,
        })

    supported = [row for row in rows if row['expected_status'] == 'answered']
    unknown = [row for row in rows if row['expected_status'] == 'abstained']
    report = {
        'dataset': dataset,
        'method': 'Roteamento para verbetes esperados em perguntas rotuladas; não mede correção factual independente.',
        'total': len(rows),
        'correct_route': sum(row['correct'] for row in supported),
        'supported_total': len(supported),
        'correct_abstention': sum(row['correct'] for row in unknown),
        'unknown_total': len(unknown),
        'grounded_answer_with_source': sum(row['has_source'] is True for row in rows),
        'actual_answered': sum(row['status'] == 'answered' for row in rows),
        'items': rows,
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', choices=['questions', 'holdout', 'challenge'], default='questions')
    args = parser.parse_args()
    report = evaluate(args.dataset)
    dest = ROOT / f'evaluation/results_{args.dataset}.json'
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Roteamento: {report['correct_route']}/{report['supported_total']}")
    print(f"Abstenção: {report['correct_abstention']}/{report['unknown_total']}")
    print(f"Respostas com fonte: {report['grounded_answer_with_source']}/{report['actual_answered']}")
    for item in report['items']:
        if not item['correct']:
            print(f"Erro {item['id']}: esperado {item['expected_article'] or item['expected_status']}, "
                  f"obtido {item['article'] or item['status']} (score={item['score']})")


if __name__ == '__main__':
    main()
