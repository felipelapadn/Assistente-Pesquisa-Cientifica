# Assistente de Pesquisa Científica com RAG

O projeto surgiu da ideia de me ajudar a descobrir novas técnicas para aplicar nos meus projetos e também explorar assuntos que são tendência no mundo da computação acadêmica. O Assistente de Pesquisa foi criado justamente para cobrir algumas limitações que ferramentas como o ChatGPT ainda apresentam, especialmente no que diz respeito à confiabilidade das informações geradas.
Muitas vezes, ao pesquisar por tópicos e artigos no ChatGPT, os links não eram apresentados, e quando apareciam, alguns estavam quebrados ou nem sequer existiam. A proposta do Assistente de Pesquisa é justamente oferecer informações confiáveis, utilizando a abordagem RAG (Retrieval-Augmented Generation) e fazendo buscas diretas em APIs de bases científicas como a ArXiv e o Semantic Scholar.

## Estrutura de pastas resumida

```
project-root/
│
├── docs/  # documentação/relatório do projeto
│   └── .pdf  
├── notebooks/  # notebooks que foram usados para investigação
│   └── .ipynb  
├── src/
│   ├── api/    # api do agente
|   ├── chat/   # controller do chat
│   ├── files/  # arquivos gerados para o RAG
│   ├── flow/   # decisão de qual API deve ser escolhida
│   ├── models/     # modelos feitos para classificar e sumarizar
│   ├── prompts/    # prompts utilizados
│   ├── rag/    # funções para realizar o RAG
│   └── utils/  # funções auxiliares 
└── main.py 
```

## Funcionalidades principais

- **Carregamento de prompts JSON:** organização dinâmica dos prompts para diferentes APIs e fluxos.
- **Leitura e processamento de PDFs:** extração e transformação em embeddings para busca.
- **Roteamento por similaridade:** escolha automática da API mais adequada para a consulta.
- **Classificação da consulta:** determina se a entrada do usuário requer resposta ou busca por artigos.
- **Sumarização de textos:** gera resumos customizáveis de textos e abstracts.
- **Geração de PDFs:** cria arquivos PDF com informações sumarizadas dos artigos consultados.
- **RAG (Retrieval-Augmented Generation):** combinação de busca por documentos relevantes com geração de texto para respostas mais precisas e contextualizadas.
- **Streaming de respostas:** entrega resposta token a token para melhor UX.
- **Interface com Streamlit:** aplicação web leve para interação com o usuário.

## Como clonar o projeto

Para clonar este repositório, use o comando:

```bash
git clone https://github.com/felipelapadn/Assistente-Pesquisa-Cientifica.git
cd Assistente-Pesquisa-Cientifica
```

## Requisitos

#### Importante: se atentar ao arquivo `.env.exemplo` da pasta `envs` para definir as variáveis de ambiente.

## Como usar

### Suba a API (build e up)

```bash
docker compose build
```

> Caso queira subir novamente sem o cache:
> ```bash
> docker compose build --no-cache
> ```

```bash
docker compose up
```

Após o up, acesse: `http://localhost:8110`

### Teste a requisição com o exemplo

No terminal, após subir a API:
```bash
python tests/exemplo_req.py
```

## Documentação do Projeto

Caso queira conferir mais sobre o projeto, acesse a pasta `docs`. 

## Autor

**Felipe Lapa do Nascimento** ([LinkedIn](https://www.linkedin.com/in/felipelapadn/) | [Email](mailto:felipelapadn@gmail.com)) 