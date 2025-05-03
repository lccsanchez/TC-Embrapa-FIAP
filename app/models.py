from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Processamentos(Base): #Definição de cada cultivo do Arquivo Processamentos
    __tablename__ = 'processamentos'

    id: Mapped[int] = mapped_column(primary_key=True)
    produto: Mapped[str] = mapped_column(String(30), nullable=False)
    categoria: Mapped[str] = mapped_column(String(20), nullable=False)
    classificacao: Mapped[str] = mapped_column(String(20), nullable=False)

    registros: Mapped[list["Registros"]] = relationship('Registros', back_populates='processamentos')

    def __repr__(self):
        return f"<Processamentos(id={self.id}, produto='{self.produto}', categoria='{self.categoria}', classificacao='{self.classificacao}')>"


class Producao(Base): #Definição de cada cultivo do Arquivo Produção
    __tablename__ = 'producao'

    id: Mapped[int] = mapped_column(primary_key=True)
    produto: Mapped[str] = mapped_column(String(30), nullable=False)
    categoria: Mapped[str] = mapped_column(String(20), nullable=False)
    classificacao: Mapped[str] = mapped_column(String(20), nullable=False)

    registros: Mapped[list["Registros"]] = relationship('Registros', back_populates='producoes')

    def __repr__(self):
        return f"<Producao(id={self.id}, produto='{self.produto}', categoria='{self.categoria}', classificacao='{self.classificacao}')>"


class Comercio(Base): #Definição de cada cultivo do Arquivo Comercialização
    __tablename__ = 'comercio'

    id: Mapped[int] = mapped_column(primary_key=True)
    produto: Mapped[str] = mapped_column(String(30), nullable=False)
    categoria: Mapped[str] = mapped_column(String(20), nullable=False)
    classificacao: Mapped[str] = mapped_column(String(20), nullable=False)

    registros: Mapped[list["Registros"]] = relationship('Registros', back_populates='Comercializacoes')

    def __repr__(self):
        return f"<Comercio(id={self.id}, produto='{self.produto}', categoria='{self.categoria}', classificacao='{self.classificacao}')>"


class Registros(Base): #Definição de quantidades por ano com base no id_cultivo
    __tablename__ = 'registros'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_produto: Mapped[int] = mapped_column(ForeignKey('processamentos.id'), nullable=False)
    ano: Mapped[int] = mapped_column(nullable=False)
    quantidade: Mapped[float] = mapped_column(nullable=False)

    processamentos: Mapped["Processamentos"] = relationship('Processamentos', back_populates='registros')
    producoes: Mapped["Producao"] = relationship('Producao', back_populates='registros')
    Comercializacoes: Mapped["Comercio"] = relationship('Comercio', back_populates='registros')

    def __repr__(self):
        return f"<Registros(id={self.id}, id_produto='{self.id_produto}', ano='{self.ano}', quantidade='{self.quantidade}')>"


class User(Base): #Definição de usuários com acesso ao sistema
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, nickname='{self.nickname}', senha='{self.senha}')>"


