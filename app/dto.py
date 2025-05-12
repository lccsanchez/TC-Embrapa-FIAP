from pydantic import BaseModel
from typing import List,Optional


class Produto(BaseModel):
    id: str
    control: str
    produto: str
    model_config = {
        "from_attributes": True
    }
   
class RegistrosDto(BaseModel):
    ano: int
    quantidade: int
    model_config = {
        "from_attributes": True
    }

class ProducaoDto(Produto):    
    registros: List[RegistrosDto]

    # Habilita suporte a ORM
    model_config = {
        "from_attributes": True
    }

class ProcessamentoDto(Produto):   
    classificacao: Optional[str] = None
    registros: List[RegistrosDto]   

    # Habilita suporte a ORM
    model_config = {
        "from_attributes": True
    }

