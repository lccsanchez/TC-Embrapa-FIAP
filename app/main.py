
from fastapi import FastAPI
from app.routes import opcoes,auth
import uvicorn 


app = FastAPI(
    title="Embrapa API",
    version="1.0.0",
    description="Extração de dados do site da Embrapa",
)

app.include_router(opcoes.router)
app.include_router(auth.router)   

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

