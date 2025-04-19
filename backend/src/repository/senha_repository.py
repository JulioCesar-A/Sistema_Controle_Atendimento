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
        print("SenhaRepositorio inicializado com db:", db)
        self.db = db


    async def contar_senhas_diario (self, senha_emitida : SenhaEmitidaCreateSchema):
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

            total_senhas = await self.contar_senhas_diario(senha_emitida)

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
            print("Definindo número de sequência...")

           


            print("Criando nova instância de Senha...")
            senha_inserir = Senha(
                numero_sequencia =  await self.definir_numero_sequencia(senha_emitida),
                tipo_senha = senha_emitida.tipo_senha.value,
                data_hora_emissao = senha_emitida.data_hora_emissao
            )
            print(f"Nova senha criada: {senha_inserir}")
            print(f"{senha_inserir.tipo_senha}")

            print("Adicionando nova senha ao banco de dados...")

            self.db.add(senha_inserir)
            await self.db.commit()
            await self.db.refresh(senha_inserir)

            print("Senha inserida com sucesso")
            return senha_inserir
        
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Erro de integridade: dados duplicados ou incorretos"
            )