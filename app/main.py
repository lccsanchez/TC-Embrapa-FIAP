
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routes import opcoes,auth
import uvicorn 


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

