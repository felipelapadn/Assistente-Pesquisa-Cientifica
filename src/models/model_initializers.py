from langchain_openai import ChatOpenAI
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


def initialize_gpt4o():
    return ChatOpenAI(model_name="gpt-4o-mini", temperature=0.6)

def initialize_pegasus():
    return pipeline("summarization", model="facebook/bart-large-cnn")