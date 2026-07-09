from fastapi import APIRouter, HTTPException
import logging
from src.api.schemas.chat import ChatRequest, ChatResponse
from src.chat.controller import ChatController 

logger = logging.getLogger(__name__)

chat_router = APIRouter(
    tags=["Chat"]
)
active_sessions = {}

def get_chat_controller(session_id: str) -> ChatController:
    """
    Retorna o controlador da sessão ou cria um novo se não existir.
    """
    if session_id not in active_sessions:
        logger.info(f"Criando nova sessão de chat: {session_id}")
        active_sessions[session_id] = ChatController(session_id=session_id)
    return active_sessions[session_id]

@chat_router.post("/orquestrador", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Recebe a mensagem do usuário, processa no ChatController e retorna a resposta da IA.
    """
    if not request.user_input.strip():
        raise HTTPException(status_code=400, detail="O campo 'user_input' não pode estar vazio.")

    try:
        controller = get_chat_controller(request.session_id)
        response_text = controller.run(user_input=request.user_input)
        
        return ChatResponse(
            session_id=request.session_id,
            response=response_text
        )
        
    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno ao processar sua mensagem.")