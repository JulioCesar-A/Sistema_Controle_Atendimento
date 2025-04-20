from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class TipoSenha(str, Enum):
    PRIORIDADE = "SP"
    GERAL = "SG"
    EXAME = "SE"

class SenhaEmitidaCreateSchema(BaseModel):
    tipo_senha : TipoSenha = Field(..., description = "Tipo de senha emitida (SP, SG, SE)"),
    data_hora_emissao : datetime = datetime.now()

    class Config:
        arbitrary_types_allowed = True

class SenhaEmitidaResponse(BaseModel):
    tipo_senha : TipoSenha
    numero_sequencia : int
    data_hora_emissao : datetime

class SenhaAtendidaCreateSchema(BaseModel):
    tipo_senha : TipoSenha
    numero_sequencia : int
    data_hora_emissao : datetime
    data_hora_atendimento : datetime = datetime.now()

    class Config:
        arbitrary_types_allowed = True

class SenhaAtendidaResponse(SenhaEmitidaResponse):
    data_hora_atendimento : Optional[datetime] = None
    tempo_atendimento : Optional[int] = None
    guiche_atendimento : Optional[str] = None

    class Config:
        from_attributes = True
