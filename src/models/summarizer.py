from src.utils.model_initializers import initialize_summa
import tensorflow as tf
import logging
from dotenv import load_dotenv
import warnings

warnings.filterwarnings('ignore')
tf.get_logger().setLevel('ERROR')
logging.basicConfig(level=logging.CRITICAL)
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

class Summarizer:
    def __init__(self):
        self.model = initialize_summa()

    def make_summarization(self, src_text, max_length=200, min_length=30, do_sample=False):
        text_to_summa = src_text[:max_length]
        result = self.model(text_to_summa, max_length=max_length, min_length=min_length, do_sample=do_sample)[0].get("summary_text")
        return result
    