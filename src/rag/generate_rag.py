import logging
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.func_aux import Auxiliar
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from src.utils.model_initializers import initialize_gpt4o

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class RAG:
    def __init__(self, tuple_similarity):
        self.aux = Auxiliar()
        self.name = tuple_similarity[1]
        self.model = initialize_gpt4o()

    def definir_prompt(self, pdf):

        prompt = ChatPromptTemplate.from_template("""
                {context} 
                {input}
                """)
        input = self.aux.load_prompt_json("rag.json")["content"].format(pdf=pdf)
        document_chain = create_stuff_documents_chain(self.model, prompt)
        return document_chain, input
    
    
    def pdf_to_vector(self, data):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=20)
        documents = text_splitter.split_documents(data)
        vector_database = FAISS.from_documents(documents, embeddings)
        retrieval = vector_database.as_retriever()

        return retrieval
        
        
    def generate_response(self): 
        pdf = self.aux.load_pdf(self.name)
        retrieval = self.pdf_to_vector(pdf)
        document_chain, input_ = self.definir_prompt(pdf)
        retrieval_chain = create_retrieval_chain(retrieval, document_chain)
        response = retrieval_chain.invoke({"input": input_})
        return response["answer"]
