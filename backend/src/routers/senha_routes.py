from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schema.senha_schemas import *
from database.database_config import get_db
from repository.senha_repository import SenhaRepositorio

router = APIRouter

router = APIRouter(
    tags=["Senhas"],
    responses={
        400: {"description": "Requisição inválida"},
        500: {"description": "Erro interno do servidor"}
    }
)


@router.post("/emitir-senha", status_code = 201, summary="Emite uma senha", response_model = SenhaEmitidaResponse)
async def emitir_senha(senha : SenhaEmitidaCreateSchema, db : AsyncSession = Depends(get_db)):
    try:
        repositorio_senha = SenhaRepositorio(db)
        resultado = await repositorio_senha.inserir_senha_emitida(senha)

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao emitir senha: {str(e)}")
    

@router.get("/", status_code=200, response_model=List[SenhaAtendidaResponse])
async def listar_todas_senhas(db : AsyncSession = Depends(get_db)):
    repositorio_senha = SenhaRepositorio(db)
    return await repositorio_senha.listar_todas_senhas()

@router.put("/{guiche}/atender-senha", status_code=200, response_model=SenhaAtendidaResponse)
async def atender_senha(senha : SenhaAtendidaCreateSchema, guiche : str, db : AsyncSession = Depends(get_db)):
    try:
        repositorio_senha = SenhaRepositorio(db)
        resultado = await repositorio_senha.atualizar_senha(senha, guiche)
        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao chamar senha: {str(e)}")