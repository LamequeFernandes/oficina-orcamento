from pydantic import BaseModel


class TipoPecaInputDTO(BaseModel):
    nome_peca: str
    peca_critica: bool


class TipoPecaOutDTO(BaseModel):
    tipo_peca_id: int | None
    nome_peca: str
    peca_critica: bool


class PecaInputDTO(BaseModel):
    tipo_peca_id: int
    valor_peca: float
    marca: str
    orcamento_id: int | None = None


class PecaOutDTO(BaseModel):
    peca_id: int | None
    valor_peca: float
    marca: str
    orcamento_id: int | None
    tipo_peca: TipoPecaOutDTO
