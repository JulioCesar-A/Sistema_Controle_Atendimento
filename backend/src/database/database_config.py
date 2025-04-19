from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_NAME = os.getenv("DATABASE_NAME", "SCC_DB")

SQLALCHEMY_DATABASE_URL = (f"mysql+asyncmy://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}")


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)


AsyncSessionLocal = sessionmaker(
    autoflush=False, autocommit=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def criar_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:    
            yield session
        except OperationalError as e:
            raise HTTPException(status_code=503, detail="Erro ao conectar ao banco de dados. O serviço se encontra indisponível")
        finally:
            await session.close()