from abc import ABC, abstractmethod
from app.modules.servico.domain.entities import Servico, TipoServico


class ServicoRepositoryInterface(ABC):
    @abstractmethod
    def salvar(self, servico: Servico) -> Servico:
        pass

    @abstractmethod
    def buscar_por_id(self, servico_id: int) -> Servico | None:
        pass

    @abstractmethod
    def remover(self, servico_id: int) -> bool:
        pass

    @abstractmethod
    def alterar(self, servico: Servico) -> Servico:
        pass

    @abstractmethod
    def vincular_a_orcamento(
        self, servico_id: int, orcamento_id: int
    ) -> Servico:
        pass

    @abstractmethod
    def desvincular_de_orcamento(self, servico_id: int) -> Servico:
        pass


class TipoServicoRepositoryInterface(ABC):
    @abstractmethod
    def salvar(self, tipo_servico: TipoServico) -> TipoServico:
        pass

    @abstractmethod
    def buscar_por_id(self, tipo_servico_id: int) -> TipoServico | None:
        pass

    @abstractmethod
    def listar(self) -> list[TipoServico]:
        pass
