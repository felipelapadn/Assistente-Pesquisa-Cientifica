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

    def make_summarization(self, src_text: str, max_length: int = 200,
                           min_length: int = 30, do_sample: bool = False) -> str:
        """
        Realiza a sumarização de um texto.

        Args:
            src_text (str): texto a ser sumarizado
            max_length (int, optional): tamanho maximo da sumarizacao. Defaults to 200.
            min_length (int, optional): tamanho minimo da sumarizacao. Defaults to 30.
            do_sample (bool, optional): _description_. Defaults to False.

        Returns:
            str: texto sumarizado
        """
        text_to_summa = src_text[:max_length]
        result = self.model(
            text_to_summa, max_length=max_length, min_length=min_length,
            do_sample=do_sample)[0].get("summary_text")
        return result
    