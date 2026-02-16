from abc import ABC, abstractmethod
from app.modules.orcamento.domain.entities import Orcamento, StatusOrcamento


class OrcamentoRepositoryInterface(ABC):
    @abstractmethod
    def salvar(self, orcamento: Orcamento) -> Orcamento:
        pass

    @abstractmethod
    def buscar_por_id(self, orcamento_id: int) -> Orcamento | None:
        pass

    # @abstractmethod
    # def alterar(self, orcamento: Orcamento) -> Orcamento:
    #     pass

    @abstractmethod
    def alterar_status(
        self, orcamento_id: int, novo_status: StatusOrcamento
    ) -> Orcamento:
        pass

    @abstractmethod
    def remover(self, orcamento_id: int) -> None:
        pass
