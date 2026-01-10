import streamlit as st
from groq import Groq
import PyPDF2

# Configuração visual do teu site
st.set_page_config(page_title="IA do Camilo", page_icon="🤖")
st.title("🤖 Chatbot Inteligente")
st.write("Sobe um PDF e eu respondo com base nele!")

# A tua chave que guardaste no ficheiro txt
CHAVE_API = "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"

client = Groq(api_key=CHAVE_API)

# Área para carregar o ficheiro
uploaded_file = st.file_uploader("Escolher ficheiro PDF", type="pdf")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Lógica para ler o PDF
pdf_text = ""
if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    st.info("Documento lido! Podes perguntar qualquer coisa.")

# Mostrar as mensagens na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de conversa
if prompt := st.chat_input("Como posso ajudar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Envia apenas uma parte do texto para não dar erro de limite
        contexto = f"Usa este texto para responder: {pdf_text[:3000]}" if pdf_text else ""
        
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "És um assistente útil em português. Podes traduzir frases e responder sobre documentos."},
                {"role": "user", "content": f"{contexto}\n\nPergunta: {prompt}"}
            ]
        )
        response = completion.choices[0].message.content
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
