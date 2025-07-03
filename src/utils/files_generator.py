# SCHOLAR E OPEN TEM PARAM E ESTRUTRA IGUAL PARA QUESITAR
# TODOS TEM A MESAM FUNÇÃO DE GERAR O PDF
# A SCHOLAR E A OPEN TEM QUE FAZER O NGC DO LATIN


# A SCHOLAR TEM QUE REESTRUTURA O RESUMO

import os
import requests
from fpdf import FPDF
import arxiv
import unicodedata
from src.models.summarizer import Summarizer

class FileGenerator:
    def __init__(self, tuple_similarity, query):
        self.tuple_similarity = tuple_similarity
        self.query = query
        self.summa = Summarizer()
    
    def clean_unicode(self, texto):
        return unicodedata.normalize('NFKD', texto).encode('latin-1', 'ignore').decode('latin-1')

    def generate_fileds(self, items, keys, abstract_transform=None, mode='dict'):
        list_infos = list()
        for item in items:
            if mode == 'dict':
                title = item.get(keys['title'])
                link = item.get(keys['link'])
                abstract_raw = item.get(keys['abstract'])
            elif mode == 'obj':
                title = getattr(item, keys['title'], None)
                link = getattr(item, keys['link'], None)
                abstract_raw = getattr(item, keys['abstract'], None)
            else:
                raise ValueError("Invalid mode: choose 'dict' or 'obj'")

            if abstract_raw is not None and abstract_transform:
                abstract = abstract_transform(abstract_raw)
            else:
                abstract = abstract_raw
                text_summa = self.summa.make_summarization(abstract, max_length=500)

            if title and link and abstract:
                list_infos.append((title, link, text_summa))

        return list_infos

    def repair_abstract(self, inverted_index):
        if not inverted_index:
            return "Resumo não disponível."
        index_map = {}
        for word, positions in inverted_index.items():
            for pos in positions:
                index_map[pos] = word
        return ' '.join(index_map[i] for i in sorted(index_map))
        
    def generate_pdf(self, list_infos):
        
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for i, (title, link, abstract) in enumerate(list_infos, 1):
            pdf.set_font("Arial", style="B", size=12)
            pdf.multi_cell(0, 10, f"Ttile: {title}")
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"Link: {link}")
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"Abstract: {self.clean_unicode(abstract)}")
            pdf.ln()

        pdf.output(f"src/files/abstracts_{self.tuple_similarity[1]}.pdf")
        
    def make_request(self):
        if self.tuple_similarity[0] == 0:
            fields_semanticscholar = {
                'title': 'title',
                'link': 'url',
                'abstract': 'abstract'
            }
            
            url = os.getenv("URL_SEMANTIC_SCHOLAR")
            params = {
                'query': self.query,
                'limit': 5,
                'fields': 'title,abstract,url'
            }

            response = requests.get(url, params=params).json()

            results = self.generate_fileds(
                items=response['data'],
                keys=fields_semanticscholar,
                mode='dict'
            )
        elif self.tuple_similarity[0] == 1:
            fields_arxiv = {
                'title': 'title',
                'link': 'entry_id',
                'abstract': 'summary'
            }
            
            search = arxiv.Search(
                query=self.query,
                max_results=5,
                sort_by=arxiv.SortCriterion.SubmittedDate,   
            )

            results = self.generate_fileds(
                items=search.results(),
                keys=fields_arxiv,
                mode='obj'
            )
            
        elif self.tuple_similarity[0] == 2:
            
            url = "https://api.openalex.org/works"
            params = {
                "filter": f"title.search:{self.query},open_access.is_oa:true",
                "per_page": 5
            }

            response = requests.get(url, params=params).json()
            
            fields_openalex = {
                'title': 'display_name',
                'link': 'doi',
                'abstract': 'abstract_inverted_index'
            }

            results = self.generate_fileds(
                items=response["results"],
                keys=fields_openalex,
                abstract_transform=self.repair_abstract,
                mode='dict'
            )
        return results
                    