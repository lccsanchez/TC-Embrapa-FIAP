"""Módulo principal da API Embrapa."""

from typing import Union

import pymysql.err
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.routes import auth, opcoes
from app.util.url.gerenciamento_estado import estado

# Definir ordem das tags
tags_metadata = [
    {
        "name": "auth",
        "description": "Operações de autenticação e autorização",
    },
    {
        "name": "opcoes",
        "description": "Operações de consulta e salvamento de dados",
    },
]

app = FastAPI(
    title="Embrapa API",
    version="1.0.0",
    description="Extração de dados do site da Embrapa",
    openapi_tags=tags_metadata,
)

app.include_router(auth.router)
app.include_router(opcoes.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", include_in_schema=False)
def root():
    """Serve a página inicial estática."""
    return FileResponse("app/static/index.html")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


@app.middleware("http")
async def intercept_all_requests(request: Request, call_next):
    """Intercepta todas as requisições para manipular o prefixo da URL."""
    estado.prefixo_url = (
        "xpto"
        if "fallback" in request.query_params
        and str.lower(request.query_params["fallback"]) == "true"
        else ""
    )
    response = await call_next(request)
    response.headers["repository"] = estado.repository
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Manipula exceções HTTPException."""
    return build_error_response(
        request=request,
        exc=exc,
        default_message=exc.detail,
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Manipula exceções genéricas."""
    return build_error_response(
        request=request,
        exc=exc,
        default_message="Erro interno no servidor",
        status_code=500,
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Manipula exceções do tipo ValueError."""
    return build_error_response(
        request=request,
        exc=exc,
        default_message="Parametro(s) inválido(s)",
        status_code=500,
    )


def build_error_response(
    request: Request,
    exc: Union[Exception, HTTPException, pymysql.err.OperationalError],
    default_message: str,
    status_code: int = None,
    custom_detail: str = None,
) -> JSONResponse:
    """Constrói uma resposta JSON para erros."""
    final_status_code = (
        status_code
        if status_code
        else (exc.status_code if isinstance(exc, HTTPException) else 500)
    )
    detail = custom_detail if custom_detail else str(exc)
    response = {
        "message": getattr(exc, "detail", default_message),
        "detail": detail,
        "type": exc.__class__.__name__,
        "path": request.url.path,
    }
    return JSONResponse(
        status_code=final_status_code,
        content=response,
    )
