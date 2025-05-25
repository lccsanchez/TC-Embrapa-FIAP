"""DTO para usuário."""

from pydantic import BaseModel


class UserDTO(BaseModel):
    """DTO para usuário."""

    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str
