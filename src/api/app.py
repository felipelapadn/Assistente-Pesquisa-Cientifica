from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from src.api.routers.chat import chat_router
import logging
logging.basicConfig(level=logging.INFO)

class AppFactory:
    """Fábrica para inicializar a API IA da INAI."""

    def __init__(self):
        
        self.route_prefix = "chat" # pode pegar esse prefix do env também
        
        self.app = FastAPI(
            title="RAG Chat API",
            description="API para orquestrar o fluxo de chat com arquitetura separada em rotas e schemas",
            version="1.0.0",
            docs_url=f"/{self.route_prefix}/docs",
            redoc_url=f"/{self.route_prefix}/redoc",
            openapi_url=f"/{self.route_prefix}/openapi.json"
        )
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self._register_routes()

        @self.app.get("/", include_in_schema=False)
        def root():
            return RedirectResponse(url=f"/{self.route_prefix}/docs")

        @self.app.get(f"/{self.route_prefix}", include_in_schema=False)
        def redirect_to_docs():
            return RedirectResponse(url=f"/{self.route_prefix}/docs")

        @self.app.get("/health", include_in_schema=False)
        def health():
            return {"status": "ok"}

    def _register_routes(self):
        """Registra os roteadores modulares (APIRouter)"""
        
        GLOBAL_PREFIX = f"/{self.route_prefix}"

        self.app.include_router(chat_router, prefix=GLOBAL_PREFIX)

    def get_app(self) -> FastAPI:
        """Retorna a instância principal do FastAPI."""
        return self.app


def create_app() -> FastAPI:
    """Função de criação da aplicação (usada pelo main.py e pelo Uvicorn no Docker)."""
    return AppFactory().get_app()
