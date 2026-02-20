from dataclasses import dataclass


@dataclass
class TipoPeca:
    tipo_peca_id: int | None
    nome_peca: str
    peca_critica: bool


@dataclass
class Peca:
    peca_id: int | None
    tipo_peca_id: int
    valor_peca: float
    marca: str
    orcamento_id: int | None = None
    tipo_peca: TipoPeca | None = None
