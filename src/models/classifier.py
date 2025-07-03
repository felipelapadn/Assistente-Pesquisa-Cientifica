from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from src.utils.func_aux import Auxiliar
from src.utils.model_initializers import initialize_gpt4o
import json

load_dotenv()

class Classificador:
    def __init__(self):
        self.aux = Auxiliar()
        self.llm = initialize_gpt4o()
    
    def classificar_mensagem(self, frase):
        prompt = self.aux.carregar_prompt_json("classificador_contexto.json")

        prompt = ChatPromptTemplate.from_template(prompt["content"])
        prompt_val = prompt.invoke({"frase": frase})
        output = self.llm.invoke(prompt_val)

        return StrOutputParser().invoke(output)
