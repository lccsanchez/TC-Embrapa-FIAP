"""DTO para totais e subitens."""

from typing import Dict, List

from pydantic import BaseModel, Field


class RegistroTotalDTO(BaseModel):
    """DTO para totais e subitens."""

    total: str = Field(..., description="Quantidade total da categoria")
    subitems: List[Dict[str, str]] = Field(
        ..., description="Lista de subitens da categoria"
    )
