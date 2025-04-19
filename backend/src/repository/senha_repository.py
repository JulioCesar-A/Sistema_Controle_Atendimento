from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.future import select
from schema.senha_schemas import SenhaEmitidaCreateSchema
from model.senha_model import Senha
from datetime import date, datetime, time



class SenhaRepositorio():

    def __init__(self, db: AsyncSession):
        self.db = db

    async def contar_senhas_diario (self, tipo_senha_emitida : str):
        try:
            inicio_dia = datetime.combine(date.today(), time.min)
            fim_dia = datetime.combine(date.today(), time.max)
            query = await self.db.execute(
                select(
                    func.count(Senha.numero_sequencia))
                    .filter(Senha.data_hora_emissao >= inicio_dia)
                    .filter(Senha.data_hora_emissao <= fim_dia)
                    .filter(Senha.tipo_senha == tipo_senha_emitida)
                )

            resultado = query.scalar()

            return resultado or 0
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail="Erro de integridade ao contar senhas.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno ao contar senhas: {str(e)}")


    async def definir_numero_sequencia (self, senha_emitida : SenhaEmitidaCreateSchema):
        try:

            total_senhas = await self.contar_senhas(senha_emitida.tipo_senha.value)

            if total_senhas == None or total_senhas == 0:
                proximo_numero = 1
            else:
                proximo_numero = total_senhas + 1

            return proximo_numero
        
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail="Erro de integridade ao definir o número da sequência")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno ao definir o número de sequência: {str(e)}")


    async def inserir_senha_emitida(self, senha_emitida : SenhaEmitidaCreateSchema):
        try:

            senha_inserir = Senha(
                senha_emitida, numero_sequencia = await self.definir_numero_sequencia(senha_emitida)
            )

            self.db.add(senha_inserir)
            self.db.commit()
            self.db.refresh(senha_inserir)

            return senha_inserir
        
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Erro de integridade: dados duplicados ou incorretos"
            )