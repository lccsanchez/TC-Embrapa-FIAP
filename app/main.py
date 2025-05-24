
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routes import opcoes,auth
import uvicorn 
from prefix import prefix
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import pymysql.err
from typing import Union

app = FastAPI(
    title="Embrapa API",
    version="1.0.0",
    description="Extração de dados do site da Embrapa",
)

app.include_router(opcoes.router)
app.include_router(auth.router)   

# Serve arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve index.html em "/"
@app.get("/", include_in_schema=False)
def root():
    return FileResponse("app/static/index.html")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
 
@app.middleware("http")
async def intercept_all_requests(request: Request, call_next): 
           
        prefix.valor = "xpto" if "fallback" in request.query_params and str.lower(request.query_params["fallback"])=="true" else ""

        return await call_next(request)      
 
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):  
    return build_error_response(
        request=request,
        exc=exc,
        default_message=exc.detail,
        status_code=exc.status_code
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return build_error_response(
        request=request,
        exc=exc,
        default_message="Erro interno no servidor",
        status_code=500
    )
@app.exception_handler(ValueError)
async def generic_exception_handler(request: Request, exc: ValueError):
    return build_error_response(
        request=request,
        exc=exc,
        default_message="Parametro(s) inválido(s)",
        status_code=500
    )

def build_error_response(
    request: Request,
    exc: Union[Exception, HTTPException, pymysql.err.OperationalError],
    default_message: str,
    status_code: int = None,
    custom_detail: str = None
) -> JSONResponse:
    
    final_status_code = status_code if status_code else (
        exc.status_code if isinstance(exc, HTTPException) else 500
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

