from src.utils.model_initializers import initialize_minilm
from src.utils.func_aux import Auxiliar
import torch

class MakeFlow:
    def __init__(self):
        self.model = initialize_minilm()
        aux = Auxiliar()
        api_definition = aux.load_prompt_json("api_definitions.json")
        self.definition = [definition for definition in api_definition.values()]
        self.names = [names for names in api_definition]
        
    def make_similarities(self, user_input: str):
        """
        Funcao que faz a similaridade com emabeddings.

        Args:
            user_input (str): entrada do usuario

        Returns:
            matriz: matriz de similariade
        """
        
        embeddings = self.model.encode(user_input)
        embedding_comparar = self.model.encode(self.definition)
        similaridades = self.model.similarity(embeddings, embedding_comparar)
        return similaridades

    def return_flow(self, similaridades):
        """
        Escolhe a API com maior similaridade.

        Args:
            similaridades (_type_): matriz de similridades.

        Returns:
            (idx, name): tupla com o index escolhido e o nome da API
        """
        _, idx = torch.max(similaridades, dim=1)
        return (idx.item(), self.names[idx])
        