from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Produto(Base):  # Classe única para Processamentos, Producao e Comercio
    __tablename__ = 'produtos'

    id: Mapped[int] = mapped_column(primary_key=True)
    produto: Mapped[str] = mapped_column(String(30), nullable=False)
    categoria: Mapped[str] = mapped_column(String(20), nullable=False)
    classificacao: Mapped[str] = mapped_column(String(20), nullable=False)

    registros: Mapped[list["Registros"]] = relationship('Registros', back_populates='produto', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Produto(id={self.id}, produto='{self.produto}', categoria='{self.categoria}', classificacao='{self.classificacao}')>"

class Registros(Base):  # Classe base para registros de ano e quantidade
    __tablename__ = 'registros'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_produto: Mapped[int] = mapped_column(ForeignKey('produtos.id'), nullable=False)  # ID do produto (genérico)
    tipo_operacao: Mapped[str] = mapped_column(String(20), nullable=False)  # Tipo do operação (processamento, produção, comércio)
    ano: Mapped[int] = mapped_column(nullable=False)
    quantidade: Mapped[float] = mapped_column(nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'registros',  # Identificador padrão para a classe base
        'polymorphic_on': tipo_operacao,  # Coluna usada para diferenciar os tipos de operação
    }

    produto: Mapped["Produto"] = relationship('Produto', back_populates='registros')

    def __repr__(self):
        return f"<Registros(id={self.id}, id_produto='{self.id_produto}', tipo_operacao='{self.tipo_operacao}', ano='{self.ano}', quantidade='{self.quantidade}')>"

class RegistroProcessamento(Registros):
    __mapper_args__ = {
        'polymorphic_identity': 'processamentos',  
    }

class RegistroProducao(Registros):
    __mapper_args__ = {
        'polymorphic_identity': 'producao', 
    }

class RegistroComercio(Registros):
    __mapper_args__ = {
        'polymorphic_identity': 'comercio',
    }

class User(Base): 
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(10), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, nickname='{self.nickname}>"


