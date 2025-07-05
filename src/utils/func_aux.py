import json
import os
from langchain_community.document_loaders import PyMuPDFLoader


class Auxiliar:
    def load_prompt_json(self, name) -> json:
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, '..', "prompts", name)
        file_path = os.path.normpath(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            prompt_json = json.load(f)
        
        return prompt_json
    
    def load_pdf(self, name) -> dict:
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, '..', "files", f"abstracts_{name}.pdf")
        file_path = os.path.normpath(file_path)
        
        loader = PyMuPDFLoader(file_path)
        data = loader.load()
        return data