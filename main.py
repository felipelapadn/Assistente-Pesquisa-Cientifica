from src.chat.controller import ChatController
import streamlit as st

chat = ChatController()

def app():
    memory = None
    st.html("""<div style='width: 50px; height: 50px; background-color:rgb(142, 161, 173); border-radius: 50%; margin-top:-5rem;'></div>""")
    st.html("""<div style='margin-top:-6rem; margin-left:5rem'>
                <p style='font-size:30px;'><b>Assistente de Pesquisa</b></p>
            </div>""")
    mensagem_usuario = st.chat_input("Digite o seu questionamento")
    if mensagem_usuario or "mensagens" in st.session_state:
        # memory, res = chat.run(memory, mensagem_usuario)
        res="ola"
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
    else:
        st.html("""<div style='text-align: center; padding-top: 10rem'>
                    <span style='font-size:30px; color:rgb(142, 161, 173)'>O que iremos pesquisar hoje?</span>
                    <br>
                    <span style='font-size:16px; color:rgb(142, 161, 173)'>Sinta-se a vontade para me perguntar sobre o mundo científico.</span>
                </div>""")


app()