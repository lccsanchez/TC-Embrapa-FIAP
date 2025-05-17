from pydantic import BaseModel, Field
from typing import Optional
from dto.registro_quantidade_valor import RegistroQuantidadeValorDTO 

class ExportacaoDTO(BaseModel):
    id: Optional[int] = Field(None, description="Identificador único da exportação")
    dados: RegistroQuantidadeValorDTO = Field(description="Dados detalhados da exportação")
