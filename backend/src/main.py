from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import senha_routes, relatorio_routes

app = FastAPI()

origins = [
    "http://127.0.0.1:3000" ,
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(senha_routes.router, prefix="/api/senha", tags=["Senhas"])
app.include_router(relatorio_routes.router, prefix="/api/relatorio", tags=["Relatórios"])