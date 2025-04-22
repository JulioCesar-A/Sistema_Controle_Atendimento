from repository.senha_repository import SenhaRepositorio
from sqlalchemy.ext.asyncio import AsyncSession
from schema.relatorio_schema import RelatorioCreate, RelatorioResponse

class RelatorioServico():
    def __init__(self, db : AsyncSession):
        self.senha_repositorio = SenhaRepositorio(db)


    async def gerar_relatorio(self, relatorio : RelatorioCreate):

        dados_relatorio = {
            "tipo_relatorio" : relatorio.tipo_relatorio.value,
            "data_referencia" : relatorio.data_referencia,
            "emitidas_prioridade" : {
                "SP" : self.senha_repositorio.contar_senhas_emitidas_por_prioridade(relatorio, "SP"),
                "SG" : self.senha_repositorio.contar_senhas_emitidas_por_prioridade(relatorio, "SG"),
                "SE" : self.senha_repositorio.contar_senhas_emitidas_por_prioridade(relatorio, "SE"),
            },
            "atentidas_prioridade" : {
                "SP" : self.senha_repositorio.contar_senhas_atendidas_por_prioridade(relatorio, "SP"),
                "SG" : self.senha_repositorio.contar_senhas_atendidas_por_prioridade(relatorio, "SG"),
                "SE" : self.senha_repositorio.contar_senhas_atendidas_por_prioridade(relatorio, "SE"),
            },
        }

        dados_relatorio["total_emitidas"] = (
            dados_relatorio["emitidas_prioridade"]["SP"]
            + dados_relatorio["emitidas_prioridade"]["SG"]
            + dados_relatorio["emitidas_prioridade"]["SE"]
        )

        dados_relatorio["total_atendidas"] = (
            dados_relatorio["atendidas_prioridade"]["SP"]
            + dados_relatorio["atendidas_prioridade"]["SG"]
            + dados_relatorio["atendidas_prioridade"]["SE"]
        )

        relatorio_gerado = RelatorioResponse(**dados_relatorio)
        
        return relatorio_gerado

    async def gerar_relatorio_mensal(self, relatorio : RelatorioCreate):

        dados_relatorio = {
            "tipo_relatorio" : relatorio.tipo_relatorio.value,
            "data_referencia" : relatorio.data_referencia,
            "emitidas_prioridade" : {
                "SP" : self.senha_repositorio.contar_senhas_emitidas_por_prioridade(relatorio, "SP"),
                "SG" : self.senha_repositorio.contar_senhas_emitidas_por_prioridade(relatorio, "SG"),
                "SE" : self.senha_repositorio.contar_senhas_emitidas_por_prioridade(relatorio, "SE"),
            },
            "atentidas_prioridade" : {
                "SP" : self.senha_repositorio.contar_senhas_atendidas_por_prioridade(relatorio, "SP"),
                "SG" : self.senha_repositorio.contar_senhas_atendidas_por_prioridade(relatorio, "SG"),
                "SE" : self.senha_repositorio.contar_senhas_atendidas_por_prioridade(relatorio, "SE"),
            },
        }

        dados_relatorio["total_emitidas"] = (
            dados_relatorio["emitidas_prioridade"]["SP"]
            + dados_relatorio["emitidas_prioridade"]["SG"]
            + dados_relatorio["emitidas_prioridade"]["SE"]
        )

        dados_relatorio["total_atendidas"] = (
            dados_relatorio["atendidas_prioridade"]["SP"]
            + dados_relatorio["atendidas_prioridade"]["SG"]
            + dados_relatorio["atendidas_prioridade"]["SE"]
        )

        relatorio_gerado = RelatorioResponse(**dados_relatorio)
        
        return relatorio_gerado
