"""DTO para token de autenticação."""

from pydantic import BaseModel


class TokenDTO(BaseModel):
    """DTO para token de autenticação."""
    access_token: str
    token_type: str
