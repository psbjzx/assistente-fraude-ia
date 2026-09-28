"""Exercita o fluxo da interface sem iniciar navegador ou servidor externo."""

from pathlib import Path

from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parent.parent / 'src/app.py'
app = AppTest.from_file(str(APP), default_timeout=25).run()
assert not app.exception, app.exception
assert len(app.chat_input) == 1

app.chat_input[0].set_value('Quantas fraudes o XGBoost encontrou no teste?').run()
assert not app.exception, app.exception
assert any('85 das 98 fraudes' in element.value and '[CASE-03]' in element.value
           for element in app.markdown)

app.chat_input[0].set_value('Minha compra de R$ 980 é fraude?').run()
assert not app.exception, app.exception
assert any('Não consigo classificar uma compra' in element.value
           for element in app.markdown)
print('Interface: pergunta suportada com fonte e abstenção específica — OK')
