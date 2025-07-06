from langchain_openai import ChatOpenAI
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from langchain.callbacks.base import BaseCallbackHandler

def initialize_gpt4o():
    return ChatOpenAI(model_name="gpt-4o-mini", temperature=0.6, streaming=True)

def initialize_summa():
    return pipeline("summarization", model="Falconsai/text_summarization")

def initialize_minilm():
    return SentenceTransformer("all-MiniLM-L6-v2")
