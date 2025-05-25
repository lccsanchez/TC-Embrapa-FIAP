"""DTO para quantidade e valor."""

from pydantic import BaseModel, Field


class RegistroQuantidadeValorDTO(BaseModel):
    """DTO para quantidade e valor."""
    quantidade: str = Field(
        ..., description="Quantidade de produtos exportados"
    )
    valor: str = Field(..., description="Valor total da exportação")
