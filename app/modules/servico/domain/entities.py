from dataclasses import dataclass


@dataclass
class TipoServico:
    tipo_servico_id: int | None
    nome_servico: str
    descricao: str | None


@dataclass
class Servico:
    servico_id: int | None
    tipo_servico_id: int
    valor_servico: float
    orcamento_id: int | None = None
    tipo_servico: TipoServico | None = None
