from typing import List
from pydantic import BaseModel, Dict
from enum import Enum
from datetime import date

from schema.senha_schemas import SenhaAtendidaResponse, TipoSenha

class TipoRelatorio(str, Enum):
    MENSAL = "M"
    DIARIO = "D"

class RelatorioBase(BaseModel):
    tipo_relatorio : TipoRelatorio
    
class RelatorioCreate(RelatorioBase):
    data_referencia : date = date.today()

class RelatorioResponse(BaseModel):
    tipo_relatorio : TipoRelatorio
    data_referencia : date
    total_emitidas : int 
    total_atendidas : int
    emitidas_prioridade : Dict[TipoSenha, int]
    atendidas_prioridade : Dict[TipoSenha, int]
    lista_detalhada : List[SenhaAtendidaResponse]