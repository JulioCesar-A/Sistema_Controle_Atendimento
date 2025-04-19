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
    data_hora_atendimento : datetime = datetime.now(),
    guiche_atendimento : str


class SenhaReponse(BaseModel):
    id_senha : int
    tipo_senha : TipoSenha
    numero_sequencia : int
    data_hora_emissao : datetime
    data_hora_atendimento : Optional[datetime] = None
    tempo_atendimento : Optional[int] = None
    guiche_atendimento : Optional[datetime] = None

    model_config = {
        "json_schema_extra" : {
            "examples" : [
                {
                    "tipo_senha" : "SP",
                    "numero_sequencia" : "1",
                    "data_hora_emissao" : "2025-04-18 21:07:47.883006"
                },
                {
                    "tipo_senha" : "SG",
                    "numero_sequencia" : "52",
                    "data_hora_emissao" : "2025-04-18 21:10:14.306505",
                    "data_hora_atendimento" : "2025-04-18 21:12:25.562812",
                    "tempo_atendimento" : "15",
                    "guiche_atendimento" : "01"
                }
            ]
        }
    }

