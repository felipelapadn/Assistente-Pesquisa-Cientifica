from langchain.memory.buffer import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.flow.flow_deciosion import MakeFlow
from src.models.classifier import Classificador
from src.rag.generate_rag import RAG
from src.utils.func_aux import Auxiliar
from src.utils.files_generator import FileGenerator
from src.utils.model_initializers import initialize_gpt4o
import logging

logging.basicConfig(level=logging.DEBUG)

class ChatController:
    
    def __init__(self):
        self.aux = Auxiliar()
        self.llm = initialize_gpt4o()
        self.classi = Classificador()
        self.flow = MakeFlow()
    
    def improve_input_quality(self, api_name: str, user_input: str, memory) -> str:
        """
        Essa funcao é responsavel por melhorar a entrada do usuario.
        O prompt para realizar esse melhoramento o faz se o usuario querer pesquisar
        por artigos, caso contrario, retorna 0.

        Args:
            api_name (str): o nome da API escolhida
            user_input (str): entrada do usuario
            memory (ConversationBufferMemory): memoria atualizada da conversa

        Returns:
            str: resposta da LLM
        """
        prompt = self.aux.load_prompt_json("improve_input_quality.json")
        prompt = ChatPromptTemplate.from_template(prompt["content"])
        prompt_val = prompt.invoke({"api": api_name, "memory": memory, "user_input": user_input})
        output = self.llm.invoke(prompt_val)

        return StrOutputParser().invoke(output)
    
    def normal_flow(self, memory, user_input: str) -> str:
        """
        A funcao aplica o normal_flow, um flow generico apenas para resposnder duvidas
        do usuário.

        Args:
            memory (ConversationBufferMemory): memoria atualizada da conversa
            user_input (str): entrada do usuario

        Returns:
            str: resposta da LLM
        """
        prompt = self.aux.load_prompt_json("normal_flow.json")
        prompt = ChatPromptTemplate.from_template(prompt["content"])
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.astream({"memory": memory, "user_input": user_input})
    
    def run(self, memory="", user_input="") -> tuple:
        """
        Funcao que roda as rotinas do chat, incluindo a classificacao da mensagem,
        escolha do flow, geracao de arquivos, RAG e o normal_flow.

        Args:
            memory (ConversationBufferMemory, optional): memoria atualizada. Defaults to None.
            user_input (str, optional): entrada do usuario. Defaults to "".

        Returns:
            (ConversationBufferMemory, str): memoria atualizada e a repsosta da LLM.
        """
        
        response = self.classi.make_classification(user_input, memory)
        
        if response:
            similarities = self.flow.make_similarities(user_input)
            choice_api = self.flow.return_flow(similarities)
            improved_user_input = self.improve_input_quality(choice_api[1], user_input, memory)
            
            if improved_user_input == "0":
                return self.normal_flow(memory, user_input)      
            try:   
                f = FileGenerator(choice_api, improved_user_input)
                results = f.make_request()
                f.generate_pdf(results)
                r = RAG(choice_api)
                return r.generate_response()
            except:
                return self.normal_flow(memory, user_input)
        else:
            return "Não entendi sua pergunta. Poderia repetir?"