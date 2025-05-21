from pydantic import BaseModel, Field
 
class RegistroQuantidadeValorDTO(BaseModel):
    quantidade: str = Field(..., description="Quantidade de produtos exportados")
    valor: str = Field(..., description="Valor total da exportação")