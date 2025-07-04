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

class ChatController:
    
    def __init__(self):
        self.aux = Auxiliar()
        self.llm = initialize_gpt4o()
    
    def improve_input_quality(self, api_name, user_input, memory):
        prompt = self.aux.load_prompt_json("improve_input_quality.json")
        prompt = ChatPromptTemplate.from_template(prompt["content"])
        prompt_val = prompt.invoke({"api": api_name, "memory": memory, "user_input": user_input})
        output = self.llm.invoke(prompt_val)

        return StrOutputParser().invoke(output)
    
    def normal_flow(self, memory, user_input):
        prompt = self.aux.load_prompt_json("normal_flow.json")
        prompt = ChatPromptTemplate.from_template(prompt["content"])
        prompt_val = prompt.invoke({"memory": memory, "user_input": user_input})
        output = self.llm.invoke(prompt_val)

        return StrOutputParser().invoke(output)
    
    def add_to_memory(self, memory, role, content):
        if role == 'user':
            message_class = HumanMessage
        elif role == 'assistant':
            message_class = AIMessage
        elif role == 'system':
            message_class = SystemMessage
        else:
            raise ValueError("Role must be 'user' or 'assistant'")
        message = message_class(content=content) 
        memory.chat_memory.add_message(message)
        return memory
    
    def run(self, memory=None, user_input=""):
        
        if memory is None:
            memory = ConversationBufferMemory()
        
        memory = self.add_to_memory(memory, "user", user_input)
        
        classi = Classificador()
        response = classi.classificar_mensagem(user_input)
        
        if response:
            flow = MakeFlow()
            similarities = flow.make_similarities(user_input)
            choice_api = flow.return_flow(similarities)
            improved_user_input = self.improve_input_quality(choice_api[1], user_input, memory)
            
            if improved_user_input == "0":
                res = self.normal_flow(memory, user_input)
                memory = self.add_to_memory(memory, "assistant", res)
                return memory, res
            
            f = FileGenerator(choice_api, improved_user_input)
            results = f.make_request()
            f.generate_pdf(results)
            try:   
                r = RAG(choice_api)
                res = r.generate_response()
            except:
                res = self.normal_flow(memory, user_input)
    
            memory = self.add_to_memory(memory, "assistant", res)
            
            return memory, res
        else:
            return memory, "Não entendi sua pergunta. Poderia repetir?"