import json

class Auxiliar:
    def carregar_prompt_json(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            prompt_json = json.load(f)
        
        return prompt_json