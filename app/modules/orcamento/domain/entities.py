from enum import StrEnum
from dataclasses import dataclass, field
from datetime import datetime

from app.modules.peca.domain.entities import Peca
from app.modules.servico.domain.entities import Servico
# from app.modules.usuario.domain.entities import Funcionario


class StatusOrcamento(StrEnum):
    AGUARDANDO_APROVACAO = 'AGUARDANDO_APROVACAO'
    APROVADO = 'APROVADO'


@dataclass
class Orcamento:
    orcamento_id: int | None
    # funcionario_id: int
    status_orcamento: StatusOrcamento
    ordem_servico_id: int
    # funcionario: Funcionario | None = None   # VER DPS SE PODE SER NULO TODO
    valor_total_orcamento: float | None = None
    dta_criacao: datetime = datetime.now()
    dta_cancelamento: datetime | None = None

    servicos: list[Servico] = field(default_factory=list)
    pecas: list[Peca] = field(default_factory=list)

    def __post_init__(self):
        soma_valor_servico = sum(
            servico.valor_servico for servico in self.servicos
        )
        soma_valor_peca = sum(peca.valor_peca for peca in self.pecas)
        self.valor_total_orcamento = soma_valor_servico + soma_valor_peca
