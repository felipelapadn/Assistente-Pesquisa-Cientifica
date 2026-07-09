from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory

from src.flow.flow_deciosion import MakeFlow
from src.models.classifier import Classificador
from src.rag.generate_rag import RAG
from src.utils.func_aux import Auxiliar
from src.utils.files_generator import FileGenerator
from src.utils.model_initializers import initialize_gpt4o
import logging

logging.basicConfig(level=logging.DEBUG)

class ChatController:
    
    def __init__(self, session_id="chat_history"):
        self.aux = Auxiliar()
        self.llm = initialize_gpt4o()
        self.classi = Classificador()
        self.flow = MakeFlow()
        
        self.message_history = FileChatMessageHistory(file_path=f"{session_id}.json")
        self.memory = ConversationBufferWindowMemory(
            k=3, 
            chat_memory=self.message_history,
            memory_key="memory",
            return_messages=False
        )
    
    def improve_input_quality(self, api_name: str, user_input: str) -> str:
        """
        Melhora a entrada do usuário com base no contexto da conversa e na API selecionada.
        """
        prompt = self.aux.load_prompt("improve_input_quality.md")
        prompt = ChatPromptTemplate.from_template(prompt)
        
        memory_content = self.memory.buffer
        
        prompt_val = prompt.invoke({"api": api_name, "memory": memory_content, "user_input": user_input})
        output = self.llm.invoke(prompt_val)

        return StrOutputParser().invoke(output)
    
    def normal_flow(self, user_input: str) -> str:
        """
        Aplica o fluxo genérico de resposta para dúvidas do usuário.
        """
        prompt = self.aux.load_prompt("normal_flow.md")
        prompt = ChatPromptTemplate.from_template(prompt)
        
        memory_content = self.memory.buffer
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"memory": memory_content, "user_input": user_input})
    
    def run(self, user_input: str = "") -> str:
        """
        Executa as rotinas principais do chat e atualiza o histórico local.
        """
        memory_content = self.memory.buffer
        response = self.classi.make_classification(user_input, memory_content)
        
        final_response = ""
        
        if response:
            similarities = self.flow.make_similarities(user_input)
            choice_api = self.flow.return_flow(similarities)
            improved_user_input = self.improve_input_quality(choice_api[1], user_input)
            
            if improved_user_input == "0":
                final_response = self.normal_flow(user_input)      
            else:
                try:   
                    f = FileGenerator(choice_api, improved_user_input)
                    results = f.make_request()
                    f.generate_pdf(results)
                    r = RAG(choice_api)
                    final_response = r.generate_response()
                except Exception as e:
                    logging.error(f"Erro no fluxo RAG: {e}")
                    final_response = self.normal_flow(user_input)
        else:
            final_response = "Não entendi sua pergunta. Poderia repetir?"
            
        self.memory.save_context({"input": user_input}, {"output": final_response})
        
        return final_response