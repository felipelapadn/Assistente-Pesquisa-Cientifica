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
        
    def make_similarities(self, user_input):
        embeddings = self.model.encode(user_input)
        embedding_comparar = self.model.encode(self.definition)
        similaridades = self.model.similarity(embeddings, embedding_comparar)
        return similaridades

    def return_flow(self, similaridades):
        _, idx = torch.max(similaridades, dim=1)
        return (idx.item(), self.names[idx])
        