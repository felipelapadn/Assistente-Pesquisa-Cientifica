import logging
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.func_aux import Auxiliar
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class RAG:
    def __init__(self, tuple_similarity):
        self.aux = Auxiliar()
        self.name = tuple_similarity[1]

    def definir_prompt(self, pdf, streaming_model):

        prompt = ChatPromptTemplate.from_template("""
                {context} 
                {input}
                """)
        input = self.aux.load_prompt_json("rag.json")["content"].format(pdf=pdf)
        document_chain = create_stuff_documents_chain(llm=streaming_model, prompt=prompt)
        return document_chain, input
    
    def pdf_to_vector(self, data):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=20)
        documents = text_splitter.split_documents(data)
        vector_database = FAISS.from_documents(documents, embeddings)
        retrieval = vector_database.as_retriever()

        return retrieval
        
    async def generate_response(self) -> str: 
        pdf = self.aux.load_pdf(self.name)
        try:
            retriever = self.pdf_to_vector(pdf)
        except:
            pdf = self.aux.load_pdf("arxiv")
            retriever = self.pdf_to_vector(pdf)

        streaming_model = ChatOpenAI(model="gpt-4o", temperature=0)
        document_chain, input_ = self.definir_prompt(pdf, streaming_model)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        async for chunk in retrieval_chain.astream({"input": input_}):
            if "answer" in chunk:
                yield chunk["answer"]
            

