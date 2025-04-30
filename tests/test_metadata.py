from app.database import Base
from app.models import Processamentos, Registros

# Verifica as tabelas registradas nos metadados
print(Base.metadata.tables.keys())