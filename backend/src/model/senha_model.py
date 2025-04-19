from sqlalchemy import Column, Enum, DATETIME, String, Integer
from schema.senha_schemas import TipoSenha
from database_config import Base

class Senha(Base):
    id = Column("ID_SENHA", Integer, primary_key = True)
    data_hora_emissao = Column("DT_HR_EM", DATETIME, nullable = False)
    tipo_senha = Column("TIPO_SENHA", Enum(TipoSenha), nullable = False)
    numero_sequencia = Column("NUM_SEQ", Integer, nullable = False)
    data_hora_atendimento = Column("DT_HR_ATEND", DATETIME, nullable = True)
    guiche_atendimento = Column("GUICHE_ATEND", String(2), nullable = True)
    tempo_atendimento = Column("TMP_ATEND", Integer, nullable = True)
    
    @classmethod
    def tipos_validos(cls):
        return [TipoSenha.EXAME.value, TipoSenha.GERAL.value, TipoSenha.PRIORIDADE.value]