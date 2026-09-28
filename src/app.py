"""Interface Streamlit. Iniciar com: streamlit run src/app.py."""

from pathlib import Path
import sys

import streamlit as st

# streamlit run src/app.py adiciona src/ ao sys.path, independentemente do cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.assistant import FraudCaseAssistant  # noqa: E402


st.set_page_config(page_title='Lupa | Entenda o case de fraude', page_icon='🔎',
                   layout='centered')


@st.cache_resource
def load_assistant() -> FraudCaseAssistant:
    return FraudCaseAssistant()


agent = load_assistant()
st.title('🔎 Lupa')
st.caption('Assistente de estudo do case de detecção de fraude em cartões')
st.info('Respostas extraídas da base local do projeto. Não analisa compras ou cartões reais.')

with st.sidebar:
    st.header('Como funciona')
    st.write('Busca por similaridade textual (TF-IDF) entre perguntas documentadas. '
             'Mostra a fonte e se abstém quando não encontra uma correspondência confiável.')
    st.write('Não utiliza LLM generativo nem pede chave de API.')
    if st.button('Limpar conversa'):
        st.session_state.messages = []
        st.rerun()

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if not st.session_state.messages:
    st.write('**Experimente uma pergunta:**')
    examples = [
        'Por que 99,8% de acurácia pode ser ruim?',
        'Quantas fraudes o XGBoost encontrou no teste?',
        'Como foi escolhido o limiar 0,189879?',
    ]
    for idx, example in enumerate(examples):
        if st.button(example, key=f'example_{idx}'):
            st.session_state.suggested_question = example
            st.rerun()

typed = st.chat_input('Pergunte sobre o case de fraude...')
question = typed or st.session_state.pop('suggested_question', None)
if question:
    st.session_state.messages.append({'role': 'user', 'content': question})
    with st.chat_message('user'):
        st.markdown(question)
    reply = agent.ask(question)
    with st.chat_message('assistant'):
        st.markdown(reply.text)
    st.session_state.messages.append({'role': 'assistant', 'content': reply.text})
