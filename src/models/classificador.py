from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def classificar_mensagem(frase):

    prompt = """Você é um agente especialista em estratégias de jogos e deve classificar a frase: {frase}; com base em seu contexto. Use as seguintes categorias:

    "Resposta genérica e sem potencial negativo" (equivalente a 1) – Frases neutras ou comuns que não oferecem risco.
    "No contexto de jogos e sem potencial negativo" (equivalente a 1) – Perguntas relacionadas a estratégias de jogos que são seguras e comuns.
    "No contexto de jogos e com potencial negativo" (equivalente a 2) – Frases que, no contexto de jogos, incentivam comportamentos problemáticos (ex.: trapaças, linguagem ofensiva).
    "Fora do contexto de jogos" (equivalente a 0) – Perguntas que não se referem a jogos ou não têm relação clara com o tema.
    "Resposta com risco potencial" (equivalente a 2) – Perguntas que indicam possível alucinação, preconceito ou perigo ao sistema, como instruções de hacking ou discursos de ódio.
    
    **Importante:** Classifique como "com risco potencial" apenas se houver evidências claras de intenção perigosa ou inadequada que vá além do contexto de jogos. Evite suposições exageradas. Se houver dúvidas, classifique a frase na categoria mais segura.
    
    Retorne somente o número da classificação, não há necessidade de textos complementares.
    """

    llm = ChatOpenAI(temperature=0.6, model='gpt-4o-mini')
    prompt = ChatPromptTemplate.from_template(prompt)
    prompt_val = prompt.invoke({"frase": frase})
    output = llm.invoke(prompt_val)

    return StrOutputParser().invoke(output)

if __name__=="__main__":
    response = classificar_mensagem('Quero estratégias para um jogo de terror com morte.')
    print(response)