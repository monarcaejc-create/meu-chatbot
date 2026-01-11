import streamlit as st
from groq import Groq
import PyPDF2

# Configuração visual do teu site
st.set_page_config(page_title="IA do Camilo", page_icon="🤖")
st.title("🤖 Chatbot Inteligente")
st.write("Sobe um PDF e eu respondo com base nele!")

# A tua chave nova (COLA A TUA CHAVE ENTRE AS ASPAS ABAIXO)
CHAVE_API = "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"

client = Groq(api_key=CHAVE_API)

# Área para carregar o ficheiro
uploaded_file = st.file_uploader("Escolher ficheiro PDF", type="pdf")

if uploaded_file is not None:
    # Ler o PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    texto_pdf = ""
    for page in pdf_reader.pages:
        texto_pdf += page.extract_text()
    
    st.success("Documento lido com sucesso!")

    # Histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensagens antigas
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada do utilizador
    if prompt := st.chat_input("Como posso ajudar?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Resposta da IA
        with st.chat_message("assistant"):
            contexto = f"Baseia-te neste texto: {texto_pdf[:5000]}\n\nPergunta: {prompt}"
            completion = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": contexto}],
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


       
