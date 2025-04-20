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

class SenhaAtendidaCreateSchema(SenhaEmitidaCreateSchema):
    numero_sequencia : int
    data_hora_atendimento : datetime = datetime.now(),
    guiche_atendimento : str

class SenhaResponse(BaseModel):
    id : int
    tipo_senha : TipoSenha
    numero_sequencia : int
    data_hora_emissao : datetime
    data_hora_atendimento : Optional[datetime] = None
    tempo_atendimento : Optional[int] = None
    guiche_atendimento : Optional[datetime] = None

    class Config:
        from_attributes = True
