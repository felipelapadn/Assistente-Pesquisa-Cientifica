from src.chat.controller import ChatController
import streamlit as st
import base64
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from time import sleep

chat = ChatController()

def stream_callback_std():
    for token in ["Não ", "entendi ", "sua ", "pergunta. ", "Poderia ", "repetir", "?"]:
        yield token
        sleep(0.05)

def app():
    file_path = "icon.png"
    
    with open(file_path, "rb") as img_file:
        img_bytes = img_file.read()
        encoded = base64.b64encode(img_bytes).decode()
        
            
    st.html(f"""<div style="position: fixed; top: 0; left: 0; width: 100%; height: 4rem; background-color: white; display: flex; align-items: center; padding: 0 1rem; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); z-index: 999;">
                    <img src="data:image/png;base64,{encoded}" alt="Logo" style="height: 2.5rem; width: 2.5rem; object-fit: contain;">
                    <p style="font-size: 1.5rem; margin-left: 1rem; margin-top:1rem; font-weight: bold; color: #000;">Assistente de Pesquisa</p>
                </div>""")
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = list()
        
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        else:
            with st.chat_message("AI"):
                st.markdown(message.content)

    
    user_input = st.chat_input("Digite o seu questionamento")
    if user_input is not None and user_input != "":
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        
        with st.chat_message("Human"):
            st.markdown(user_input)
        
        with st.chat_message("AI"):
            try:
                ai_response = st.write_stream(chat.run(st.session_state.chat_history, user_input))
            except:
                ai_response = st.write_stream(stream_callback_std())
        st.session_state.chat_history.append(AIMessage(content=ai_response))

    if st.session_state.chat_history == []:
        st.html("""<div style='text-align: center; margin-top: 30%'>
                    <span style='font-size:30px; color:rgb(142, 161, 173)'>O que iremos pesquisar hoje?</span>
                    <br>
                    <span style='font-size:16px; color:rgb(142, 161, 173)'>Sinta-se à vontade para me perguntar sobre o mundo científico.</span>
                </div>""")


app()
