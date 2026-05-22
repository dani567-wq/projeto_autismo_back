from pydantic import BaseModel, ConfigDict


class DiarioEntryCreate(BaseModel):
    tipo: str
    data: str
    conteudo: str  # JSON string com os dados do formulário


class DiarioEntryPublic(BaseModel):
    id: int
    tipo: str
    data: str
    conteudo: str
    model_config = ConfigDict(from_attributes=True)


class DiarioList(BaseModel):
    entries: list[DiarioEntryPublic]
