import json
import os
from langchain_community.document_loaders import PyMuPDFLoader
from typing import Dict

class Auxiliar:
    def load_prompt_json(self, name: str) -> Dict:
        """
        Carrega um arquivo JSON de prompt a partir da pasta 'prompts'.

        Args:
            name (str): Nome do arquivo JSON do prompt.

        Returns:
            Dict: Conteúdo do arquivo JSON carregado.
        """
            
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, '..', "prompts", name)
        file_path = os.path.normpath(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            prompt_json = json.load(f)
        
        return prompt_json
    
    def load_pdf(self, name) -> dict:
        """
        Carrega o conteúdo de um PDF localizado na pasta 'files' com prefixo 'abstracts_'.

        Args:
            name (str): Nome base do arquivo PDF (sem prefixo).

        Returns:
            Dict: Dados extraídos do PDF via PyMuPDFLoader.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, '..', "files", f"abstracts_{name}.pdf")
        file_path = os.path.normpath(file_path)
        
        loader = PyMuPDFLoader(file_path)
        data = loader.load()
        return data