from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from service.relatorio_service import RelatorioServico
from database.database_config import get_db
from schema.relatorio_schema import RelatorioCreate, RelatorioResponse

router = APIRouter(
    tags=["Relatórios"],
    responses={
        400: {"description": "Requisição inválida"},
        500: {"description": "Erro interno do servidor"} 
    }
)

@router.post("/gerar-relatorio", status_code = 200, response_model = RelatorioResponse)
async def gerar_relatorio(relatorio : RelatorioCreate, db : AsyncSession = Depends(get_db)):
    try:
        servico_relatorio = RelatorioServico(db)

        resultado = await servico_relatorio.gerar_relatorio_diario(relatorio)

        return resultado
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Erro ao gerar relatório: {str(e)}")
