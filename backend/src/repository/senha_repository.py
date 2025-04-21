from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, null
from sqlalchemy.future import select
from schema.relatorio_schema import RelatorioCreate
from schema.senha_schemas import *
from model.senha_model import Senha
from datetime import date, datetime, time
import random
import calendar

class SenhaRepositorio():
    def __init__(self, db: AsyncSession):
        print("SenhaRepositorio inicializado com db:", db)
        self.db = db



    async def contar_senhas (self, senha_emitida : SenhaEmitidaCreateSchema):
        try:
            inicio_dia = datetime.combine(date.today(), time.min)
            fim_dia = datetime.combine(date.today(), time.max)
            query = await self.db.execute(
                select(
                    func.count(Senha.numero_sequencia))
                    .filter(Senha.data_hora_emissao >= inicio_dia)
                    .filter(Senha.data_hora_emissao <= fim_dia)
                    .filter(Senha.tipo_senha == senha_emitida.tipo_senha.value)
                )

            resultado = query.scalar()

            return resultado or 0
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail="Erro de integridade ao contar senhas.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno ao contar senhas: {str(e)}")


    async def definir_numero_sequencia (self, senha_emitida : SenhaEmitidaCreateSchema):
        try:
            total_senhas = await self.contar_senhas(senha_emitida)

            if total_senhas == None or total_senhas == 0:
                proximo_numero = 1
            else:
                proximo_numero = total_senhas + 1

            return proximo_numero
        
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail="Erro de integridade ao definir o número da sequência")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno ao definir o número de sequência: {str(e)}")
        
    async def definir_tempo_atendimento(self, tipo_senha : str):
        if tipo_senha == "SG":
            
            # Base: 5 minutos (-+ 3 minutos)
            return random.randint(2, 8)
        
        elif tipo_senha == "SP":

            # Base: 15 minutos (-+ 5 minutos)
            return random.randint(10, 20)

        elif tipo_senha == "SE":

            # 95% dos atendimentos tem 1 minuto, os 5% restantes tem 5 minutos
            if random.random() < 0.95:
                return 1
            else:
                return 5
            
        else:
            raise ValueError("Tipo de senha inválido. Valores Aceitos: 'SP', 'SG', 'SE'.")
        

    # função para testes (apenas)
    async def listar_todas_senhas(self):
        query = await self.db.execute(select(Senha))
        senhas = query.scalars().all()
        return [SenhaAtendidaResponse.model_validate(senha) for senha in senhas]
        

    async def buscar_senha(self, numero_sequencia : int, tipo_senha : str):
        inicio_dia = datetime.combine(date.today(), time.min)
        fim_dia = datetime.combine(date.today(), time.max)
        query = await self.db.execute(select(Senha)
                                      .filter(Senha.numero_sequencia == numero_sequencia)
                                      .filter(Senha.tipo_senha == tipo_senha)
                                      .filter(Senha.data_hora_emissao >= inicio_dia)
                                      .filter(Senha.data_hora_emissao <= fim_dia))
        senha_existente = query.scalars().first()

        return senha_existente


    async def inserir_senha_emitida(self, senha_emitida : SenhaEmitidaCreateSchema):
        try:
            senha_inserir = Senha(
                numero_sequencia =  await self.definir_numero_sequencia(senha_emitida),
                tipo_senha = senha_emitida.tipo_senha.value,
                data_hora_emissao = senha_emitida.data_hora_emissao
            )

            self.db.add(senha_inserir)
            await self.db.commit()
            await self.db.refresh(senha_inserir)

            return senha_inserir
        
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Erro de integridade: dados duplicados ou incorretos"
            )
        
    async def atualizar_senha(self, senha_atendida : SenhaAtendidaCreateSchema, guiche : str):
        senha_existente = await self.buscar_senha(senha_atendida.numero_sequencia, senha_atendida.tipo_senha.value)
        
        if senha_existente:
            senha_existente.data_hora_atendimento = senha_atendida.data_hora_atendimento
            senha_existente.tempo_atendimento = await self.definir_tempo_atendimento(senha_existente.tipo_senha)
            senha_existente.guiche_atendimento = guiche

            await self.db.commit()
            await self.db.refresh(senha_existente)
            return senha_existente
        
        else:
            raise ValueError("Senha não encontrada.")
        

    # Funções para relatório
    async def contar_senhas_emitidas_por_prioridade(self, relatorio : RelatorioCreate, prioridade : str):
        try:
            if relatorio.tipo_relatorio.value == "M":

                _, ultimo_dia = calendar.monthrange(relatorio.data_referencia.year, relatorio.data_referencia.month)

                inicio_mes = datetime.combine(date(relatorio.data_referencia.year, relatorio.data_referencia.month, 1), time.min)

                fim_mes = datetime.combine(date(relatorio.data_referencia.year, relatorio.data_referencia.month, ultimo_dia), time.max)


                query = await self.db.execute(
                    select(
                        func.count(Senha.numero_sequencia)
                        .filter(Senha.tipo_senha == prioridade)
                        .filter(Senha.data_hora_emissao >= inicio_mes)
                        .filter(Senha.data_hora_emissao <= fim_mes)
                    ))

                resultado = query.scalar()

                return resultado or 0

            
            elif relatorio.tipo_relatorio.value == "D":
                query = await self.db.execute(
                    select(
                        func.count(Senha.numero_sequencia)
                        .filter(Senha.tipo_senha == prioridade)
                        .filter(Senha.data_hora_emissao >= datetime.combine(relatorio.data_referencia, time.min))
                        .filter(Senha.data_hora_emissao <= datetime.combine(relatorio.data_referencia, time.max))
                    )
                )

                resultado = query.scalar()

                return resultado or 0        
            else:
                raise ValueError("Tipo de Relatório Inválido. Valores Aceitos: 'M','D'")
            
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail="Erro de integridade ao contar senhas emitidas.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno ao contar senhas emitidas: {str(e)}")


    async def contar_senhas_atendidas_por_prioridade(self, relatorio : RelatorioCreate, prioridade : str):
        try:
            if relatorio.tipo_relatorio.value == "M":

                _, ultimo_dia = calendar.monthrange(relatorio.data_referencia.year, relatorio.data_referencia.month)

                inicio_mes = datetime.combine(date(relatorio.data_referencia.year, relatorio.data_referencia.month, 1), time.min)

                fim_mes = datetime.combine(date(relatorio.data_referencia.year, relatorio.data_referencia.month, ultimo_dia), time.max)


                query = await self.db.execute(
                    select(
                        func.count(Senha.numero_sequencia)
                        .filter(Senha.tipo_senha == prioridade)
                        .filter(Senha.data_hora_emissao >= inicio_mes)
                        .filter(Senha.data_hora_emissao <= fim_mes)
                        .filter(Senha.data_hora_atendimento != null)
                    ))

                resultado = query.scalar()

                return resultado or 0

            
            elif relatorio.tipo_relatorio.value == "D":
                query = await self.db.execute(
                    select(
                        func.count(Senha.numero_sequencia)
                        .filter(Senha.tipo_senha == prioridade)
                        .filter(Senha.data_hora_emissao >= datetime.combine(relatorio.data_referencia, time.min))
                        .filter(Senha.data_hora_emissao <= datetime.combine(relatorio.data_referencia, time.max))
                        .filter(Senha.data_hora_atendimento != null)
                    )
                )

                resultado = query.scalar()

                return resultado or 0        
            else:
                raise ValueError("Tipo de Relatório Inválido. Valores Aceitos: 'M','D'")
            
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail="Erro de integridade ao contar senhas atendidas.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno ao contar senhas atendidas: {str(e)}")
        
    async def listar_senhas(self, relatorio : RelatorioCreate):
        try:
            if relatorio.tipo_relatorio.value == "M":

                _, ultimo_dia = calendar.monthrange(relatorio.data_referencia.year, relatorio.data_referencia.month)

                inicio_mes = datetime.combine(date(relatorio.data_referencia.year, relatorio.data_referencia.month, 1), time.min)

                fim_mes = datetime.combine(date(relatorio.data_referencia.year, relatorio.data_referencia.month, ultimo_dia), time.max)


                query = await self.db.execute(select(Senha)
                    .filter(Senha.data_hora_emissao >= inicio_mes)
                    .filter(Senha.data_hora_emissao <= fim_mes)
                )

                resultado = query.scalars().all()

                return resultado or None

            
            elif relatorio.tipo_relatorio.value == "D":
                query = await self.db.execute(select(Senha)
                    .filter(Senha.data_hora_emissao >= datetime.combine(date.today(), time.min))
                    .filter(Senha.data_hora_emissao <=  datetime.combine(date.today(), time.max))
                )

                resultado = query.scalars().all()

                return resultado or None     
            else:
                raise ValueError("Tipo de Relatório Inválido. Valores Aceitos: 'M','D'")
            
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail="Erro de integridade ao listar senhas.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno ao listar senhas: {str(e)}")