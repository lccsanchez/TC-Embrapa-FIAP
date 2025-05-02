from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Processamentos(Base): #Definição de cada cultivo do Arquivo Processamentos
    __tablename__ = 'processamentos'

    id: Mapped[int] = mapped_column(primary_key=True)
    cultivo: Mapped[str] = mapped_column(String(30), nullable=False)
    categoria: Mapped[str] = mapped_column(String(20), nullable=False)
    classificacao: Mapped[str] = mapped_column(String(20), nullable=False)

    registros: Mapped[list["Registros"]] = relationship('Registros', back_populates='processamentos')

class Registros(Base): #Definição de quantidades por ano com base no id_cultivo
    __tablename__ = 'registros'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_cultivo: Mapped[int] = mapped_column(ForeignKey('processamentos.id'), nullable=False)
    ano: Mapped[int] = mapped_column(nullable=False)
    quantidade: Mapped[float] = mapped_column(nullable=False)

    processamentos: Mapped["Processamentos"] = relationship('Processamentos', back_populates='registros')
