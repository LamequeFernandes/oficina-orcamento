from pydantic import BaseModel


class TipoServicoInputDTO(BaseModel):
    nome_servico: str
    descricao: str | None = None


class TipoServicoOutDTO(BaseModel):
    tipo_servico_id: int | None
    nome_servico: str
    descricao: str | None


class ServicoInputDTO(BaseModel):
    tipo_servico_id: int
    valor_servico: float
    orcamento_id: int


class ServicoOutDTO(BaseModel):
    servico_id: int | None
    valor_servico: float
    orcamento_id: int | None = None
    tipo_servico: TipoServicoOutDTO
