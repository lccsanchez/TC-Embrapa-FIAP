from sqlalchemy import String, ForeignKey,Integer,Boolean,Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from decimal import Decimal
Base = declarative_base()

class Produto(Base):  # Classe única para Processamentos, Producao e Comercio
    __tablename__ = 'produtos'

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    source_id: Mapped[int] = mapped_column(Integer, nullable=True)  # Remova primary_key=True
    control: Mapped[str] = mapped_column(String(100), nullable=True)
    produto: Mapped[str] = mapped_column(String(200), nullable=True)
    categoria: Mapped[str] = mapped_column(String(100), nullable=True)
    classificacao: Mapped[str] = mapped_column(String(100), nullable=True)

    registros: Mapped[list["Registros"]] = relationship('Registros', back_populates='produto', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Produto(id={self.id}, produto='{self.produto}', categoria='{self.categoria}', classificacao='{self.classificacao}')>"

class Registros(Base):  # Classe base para registros de ano e quantidade
    __tablename__ = 'registros'

    id: Mapped[str] = mapped_column(String(50),primary_key=True)
    id_produto: Mapped[str] = mapped_column(ForeignKey('produtos.id', ondelete="CASCADE"), nullable=False)  # ID do produto (genérico)
    tipo_operacao: Mapped[str] = mapped_column(String(20), nullable=False)  # Tipo do operação (processamento, produção, comércio)
    ano: Mapped[int] = mapped_column(nullable=False)
    quantidade: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=0), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'registros',  # Identificador padrão para a classe base
        'polymorphic_on': tipo_operacao,  # Coluna usada para diferenciar os tipos de operação
    }

    produto: Mapped["Produto"] = relationship('Produto', back_populates='registros')

    def __repr__(self):
        return f"<Registros(id={self.id}, id_produto='{self.id_produto}', tipo_operacao='{self.tipo_operacao}', ano='{self.ano}', quantidade='{self.quantidade}')>"

class RegistroProcessamento(Registros):
    __mapper_args__ = {
        'polymorphic_identity': 'processamento',  
    }
    def __init__(self, tipo_operacao: str = 'processamento', **kwargs):
        super().__init__(tipo_operacao=tipo_operacao, **kwargs)

class RegistroProducao(Registros):
    __mapper_args__ = {
        'polymorphic_identity': 'producao', 
    }
    def __init__(self, tipo_operacao: str = 'producao', **kwargs):
        super().__init__(tipo_operacao=tipo_operacao, **kwargs)

class RegistroComercio(Registros):
    __mapper_args__ = {
        'polymorphic_identity': 'comercio',
    }
    def __init__(self, tipo_operacao: str = 'comercio', **kwargs):
        super().__init__(tipo_operacao=tipo_operacao, **kwargs)

class ImportacaoExportacao(Base):  # Classe única para Importação e Exportação
    __tablename__ = "importacao_exportacao"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    source_id: Mapped[int] = mapped_column(Integer, nullable=True)  # Remova primary_key=True
    pais: Mapped[str] = mapped_column(String(200), nullable=False)
    classificacao: Mapped[str] = mapped_column(String(100), nullable=True)

    registros_imp_exp: Mapped[list["RegistroImportacaoExportacao"]] = relationship(
        "RegistroImportacaoExportacao", back_populates="pais", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<ImportacaoExportacao(id={self.id}, pais='{self.pais}', classificacao='{self.classificacao}')>"

class RegistroImportacaoExportacao(Base):
    __tablename__ = "registros_importacao_exportacao"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    id_pais: Mapped[str] = mapped_column(
        ForeignKey("importacao_exportacao.id", ondelete="CASCADE"), nullable=False
    )
    tipo_operacao: Mapped[str] = mapped_column(String(20), nullable=False)  # Tipo do operação (importacao, exportacao)
    ano: Mapped[int] = mapped_column(nullable=False)
    quantidade: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=0), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=2), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'registros_imp_exp',  # Identificador padrão para a classe base
        'polymorphic_on': tipo_operacao,  # Coluna usada para diferenciar os tipos de operação
    }

    pais: Mapped["ImportacaoExportacao"] = relationship(
        "ImportacaoExportacao", back_populates="registros_imp_exp"
    )

    def __repr__(self):
        return (
            f"<RegistroImportacaoExportacao(id={self.id}, id_pais='{self.id_pais}', "
            f"tipo_operacao='{self.tipo_operacao}', ano='{self.ano}', "
            f"quantidade='{self.quantidade}', valor='{self.valor}')>"
        )

class RegistroImportacao(RegistroImportacaoExportacao):
    __mapper_args__ = {
        'polymorphic_identity': 'importacao',  
    }
    def __init__(self, tipo_operacao: str = 'importacao', **kwargs):
        super().__init__(tipo_operacao=tipo_operacao, **kwargs)  

class RegistroExportacao(RegistroImportacaoExportacao):
    __mapper_args__ = {
        "polymorphic_identity": "exportacao",
    }
    def __init__(self, tipo_operacao: str = 'exportacao', **kwargs):
        super().__init__(tipo_operacao=tipo_operacao, **kwargs)    

class Users(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True, index=True)
    email = mapped_column(String(100), unique=True)
    username = mapped_column(String(100), unique=True)
    first_name = mapped_column(String(100))
    last_name = mapped_column(String(100))
    hashed_password = mapped_column(String(100))
    is_active = mapped_column(Boolean, default=True)
    role = mapped_column(String(50))
    phone_number = mapped_column(String(50))
