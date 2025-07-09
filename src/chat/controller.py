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
        Melhora a entrada do usuário com base no contexto da conversa e na API selecionada.
        Caso a entrada não esteja relacionada à busca por artigos, retorna uma resposta padrão.

        Args:
            api_name (str): Nome da API selecionada (ex: "scientific", "news", etc.).
            user_input (str): Texto fornecido pelo usuário.
            memory (ConversationBufferMemory): Objeto de memória que armazena o histórico da conversa.

        Returns:
            str: Entrada do usuário aprimorada ou resposta padrão, gerada pela LLM.
        """
        prompt = self.aux.load_prompt_json("improve_input_quality.json")
        prompt = ChatPromptTemplate.from_template(prompt["content"])
        prompt_val = prompt.invoke({"api": api_name, "memory": memory, "user_input": user_input})
        output = self.llm.invoke(prompt_val)

        return StrOutputParser().invoke(output)
    
    def normal_flow(self, memory, user_input: str) -> str:
        """
        Aplica o fluxo genérico de resposta para dúvidas do usuário, utilizando o contexto da conversa.

        Args:
            memory (ConversationBufferMemory): Objeto de memória com o histórico da conversa.
            user_input (str): Entrada textual fornecida pelo usuário.

        Returns:
            str: Resposta gerada pela LLM com base na entrada do usuário e na memória da conversa.
        """
        prompt = self.aux.load_prompt_json("normal_flow.json")
        prompt = ChatPromptTemplate.from_template(prompt["content"])
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.astream({"memory": memory, "user_input": user_input})
    
    def run(self, memory="", user_input="") -> str:
        """
        Executa as rotinas principais do chat, incluindo classificação da mensagem, 
        escolha do fluxo apropriado, geração de arquivos, execução do RAG e fallback para o fluxo normal.

        Args:
            memory (ConversationBufferMemory, optional): Objeto de memória com o histórico da conversa. Defaults to None.
            user_input (str, optional): Entrada textual fornecida pelo usuário. Defaults to "".

        Returns:
            str: Resposta gerada pela LLM.
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