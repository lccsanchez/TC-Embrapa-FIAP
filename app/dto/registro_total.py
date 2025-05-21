from pydantic import BaseModel, Field
from typing import List,Dict

class RegistroTotalDTO(BaseModel):
    total: str = Field(..., description="Quantidade total da categoria")
    subitems: List[Dict[str,str]] = Field(..., description="Lista de subitens da categoria")