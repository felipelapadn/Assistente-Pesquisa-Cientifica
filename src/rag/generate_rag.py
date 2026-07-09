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
        """
        Define e prepara o prompt para o modelo de streaming com base no conteúdo do PDF.

        Args:
            pdf (bytes): Conteúdo do arquivo PDF em formato binário.
            streaming_model (object): Instância do modelo que processará o prompt.

        Returns:
            str: Prompt formatado pronto para ser enviado ao modelo.
        """
        prompt = ChatPromptTemplate.from_template("""
                {context} 
                {input}
                """)
        input = self.aux.load_prompt("rag.md").format(pdf=pdf)
        document_chain = create_stuff_documents_chain(llm=streaming_model, prompt=prompt)
        return document_chain, input
    
    def pdf_to_vector(self, data):
        """
        Transforma um PDF em embeddings para armazenar no FAISS e retorna o retriever associado.

        Args:
            pdf (bytes): Conteúdo do arquivo PDF em formato binário.

        Returns:
            object: Objeto retriever para consulta dos embeddings armazenados.
        """
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=20)
        documents = text_splitter.split_documents(data)
        vector_database = FAISS.from_documents(documents, embeddings)
        retrieval = vector_database.as_retriever()

        return retrieval
        
    async def generate_response(self) -> str: 
        """
        Cria a chain que realiza o RAG (Retrieval-Augmented Generation) 
        e retorna tokens da resposta gerada em streaming, um a um.

        Yields:
            str: Token gerado da resposta, emitido incrementalmente.
        """
        pdf = self.aux.load_pdf(self.name)
        try:
            retriever = self.pdf_to_vector(pdf)
        except:
            pdf = self.aux.load_pdf("arxiv")
            retriever = self.pdf_to_vector(pdf)

        streaming_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        document_chain, input_ = self.definir_prompt(pdf, streaming_model)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        return retrieval_chain.invoke({"input": input_})
            

