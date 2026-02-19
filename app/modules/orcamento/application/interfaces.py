from abc import ABC, abstractmethod
from app.modules.orcamento.domain.entities import Orcamento, StatusOrcamento


class OrcamentoRepositoryInterface(ABC):
    @abstractmethod
    def salvar(self, orcamento: Orcamento) -> Orcamento:
        pass

    @abstractmethod
    def buscar_por_id(self, orcamento_id: int) -> Orcamento | None:
        pass

    @abstractmethod
    def buscar_por_preference_id(self, preference_id: str) -> Orcamento | None:
        pass

    @abstractmethod
    def alterar_status(
        self, orcamento_id: int, novo_status: StatusOrcamento
    ) -> Orcamento:
        pass

    @abstractmethod
    def atualizar_dados_pagamento(
        self,
        orcamento_id: int,
        url_pagamento: str | None,
        preference_id: str | None,
    ) -> None:
        pass

    @abstractmethod
    def marcar_como_pago(
        self,
        orcamento_id: int,
        mp_payment_id: str,
    ) -> Orcamento:
        pass

    @abstractmethod
    def remover(self, orcamento_id: int) -> None:
        pass
