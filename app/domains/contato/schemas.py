from pydantic import BaseModel, ConfigDict


class ContatoCreate(BaseModel):
    nome: str
    telefone: str
    idade: str = ''
    tipo: str = ''
    mensagem: str = ''


class ContatoPublic(BaseModel):
    id: int
    nome: str
    telefone: str
    mensagem: str
    model_config = ConfigDict(from_attributes=True)
