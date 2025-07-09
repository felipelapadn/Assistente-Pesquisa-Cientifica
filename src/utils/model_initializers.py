from langchain_openai import ChatOpenAI
from transformers import pipeline
from sentence_transformers import SentenceTransformer

def initialize_gpt4o():
    """
    Inicializa e retorna uma instância do modelo ChatOpenAI GPT-4o-mini configurado para streaming.

    Returns:
        ChatOpenAI: Instância configurada do modelo GPT-4o-mini.
    """
    return ChatOpenAI(model_name="gpt-4o-mini", temperature=0.6, streaming=True)


def initialize_summa():
    """
    Inicializa e retorna um pipeline de sumarização usando o modelo 'Falconsai/text_summarization'.

    Returns:
        object: Pipeline de sumarização do Hugging Face Transformers.
    """
    return pipeline("summarization", model="Falconsai/text_summarization")


def initialize_minilm():
    """
    Inicializa e retorna uma instância do modelo SentenceTransformer 'all-MiniLM-L6-v2'.

    Returns:
        SentenceTransformer: Instância do modelo de embeddings.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")

