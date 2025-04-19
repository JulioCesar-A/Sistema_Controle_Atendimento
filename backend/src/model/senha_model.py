from sqlalchemy import Column, Enum, DateTime, String, Integer
from schema.senha_schemas import TipoSenha
from database.database_config import Base

class Senha(Base):
    __tablename__ = "SENHA_TB"
    
    id = Column("ID_SENHA", Integer, primary_key = True)
    data_hora_emissao = Column("DT_HR_EM", DateTime, nullable = False)
    tipo_senha = Column("TIPO_SENHA", String(2), nullable = False)
    numero_sequencia = Column("NUM_SEQ", Integer, nullable = False)
    data_hora_atendimento = Column("DT_HR_ATEND", DateTime, nullable = True)
    guiche_atendimento = Column("GUICHE_ATEND", String(2), nullable = True)
    tempo_atendimento = Column("TMP_ATEND", Integer, nullable = True)
    
    