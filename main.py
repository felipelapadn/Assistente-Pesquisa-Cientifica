
from src.chat.controller import ChatController


chat = ChatController()

import streamlit as st

def app():
    st.header(f"Pesquisador")
    memory = None
    mensagem_usuario = st.chat_input("Diga tudo")

    if mensagem_usuario:
        memory, res = chat.run(memory, mensagem_usuario)
        if "mensagens" in st.session_state:
            mensagens = st.session_state["mensagens"]
        else:
            mensagens = list()
            st.session_state["mensagens"] = mensagens
            
        mensagens.append({"usuario": "user", "texto": mensagem_usuario})
        mensagens.append({"usuario": "assistant", "texto": res})
        
        for mensagem in mensagens:            
            with st.chat_message(mensagem["usuario"]):
                st.write(mensagem["texto"])
        
            
app()
            

        
    