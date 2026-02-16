from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    ApenasMecanicoResponsavel,
    NaoEncontradoError,
    ValorDuplicadoError,
)
from app.core.utils import obter_valor_e_key_duplicado_integrity_error
# from app.modules.usuario.infrastructure.models import ClienteModel, FuncionarioModel
# from app.modules.ordem_servico.infrastructure.models import OrdemServicoModel

from app.modules.orcamento.application.dto import (
    OrcamentoInputDTO,
    OrcamentoOutputDTO,
)
from app.modules.orcamento.infrastructure.mapper import OrcamentoMapper

from app.modules.orcamento.domain.entities import Orcamento, StatusOrcamento
from app.modules.orcamento.infrastructure.repositories import (
    OrcamentoRepository,
)


class CriarOrcamentoUseCase:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrcamentoRepository(db)

    # def validar_ordem_servico_vinculada(self, ordem_servico_id: int) -> None:
    #     ordem_servico = (
    #         self.db.query(OrdemServicoModel)
    #         .filter(OrdemServicoModel.ordem_servico_id == ordem_servico_id)
    #         .first()
    #     )
    #     if not ordem_servico:
    #         raise NaoEncontradoError('Ordem de Serviço', ordem_servico_id)

    #     if ordem_servico.orcamento:
    #         raise ValueError(
    #             'Ordem de Serviço já possui um orçamento vinculado.'
    #         )

    # def validar_funcionario_vinculado(self, funcionario_id: int) -> None:
    #     funcionario = (
    #         self.db.query(FuncionarioModel)
    #         .filter(FuncionarioModel.funcionario_id == funcionario_id)
    #         .first()
    #     )
    #     if not funcionario:
    #         raise NaoEncontradoError('Funcionário', funcionario_id)
    #     if funcionario.tipo_funcionario != 'MECANICO': # type: ignore
    #         raise ValueError('Funcionário não é um mecânico.')

    def executar(
        self, dados: OrcamentoInputDTO
    ) -> OrcamentoOutputDTO:
        orcamento = Orcamento(
            orcamento_id=None,
            # funcionario_id=dados.funcionario_id,
            status_orcamento=dados.status_orcamento,
            ordem_servico_id=dados.ordem_servico_id,
        )
        # self.validar_ordem_servico_vinculada(ordem_servico_id)
        # self.validar_funcionario_vinculado(dados.funcionario_id)

        try:
            orcamento_salvo = self.repo.salvar(orcamento)
        except IntegrityError as e:
            (
                valor_duplicado,
                chave,
            ) = obter_valor_e_key_duplicado_integrity_error(e)
            raise ValorDuplicadoError(valor_duplicado, chave)
        return OrcamentoMapper.entity_to_output_dto(orcamento_salvo)


class BuscarOrcamentoUseCase:
    def __init__(self, db: Session):
        self.repo = OrcamentoRepository(db)

    def executar(self, orcamento_id: int) -> OrcamentoOutputDTO:
        orcamento = self.repo.buscar_por_id(orcamento_id)
        if not orcamento:
            raise NaoEncontradoError('Orçamento', orcamento_id)
        return OrcamentoMapper.entity_to_output_dto(orcamento)


class AlterarStatusOrcamentoUseCase:
    def __init__(self, db: Session):
        self.repo = OrcamentoRepository(db)
        # self.mecanico_logado = mecanico_logado

    # def eh_mecanico_responsavel(self, orcamento: Orcamento) -> bool:
    #     return orcamento.funcionario_id == self.mecanico_logado.funcionario_id

    # def eh_cliente_dono_ordem_servico(self, orcamento: Orcamento) -> bool:
    #     for veiculo in self.cliente_logado.veiculos:
    #         for ordem in veiculo.ordens_servico:
    #             if ordem.ordem_servico_id == orcamento.ordem_servico_id:
    #                 return True
    #     return False

    # def validar_alteracao(self, orcamento: Orcamento) -> None:
    #     # if not self.eh_mecanico_responsavel(orcamento):
    #     #     raise ApenasMecanicoResponsavel
    #     if not self.eh_cliente_dono_ordem_servico(orcamento):
    #         raise ValueError(
    #             'Apenas o cliente dono da ordem de serviço pode alterar o status do orçamento.'
    #         )
    #     if orcamento.status_orcamento == StatusOrcamento.APROVADO:
    #         raise ValueError(
    #             'Não é possível alterar o status de um orçamento que já foi aprovado.'
    #         )

    def executar(
        self, orcamento_id: int, status: StatusOrcamento
    ) -> OrcamentoOutputDTO:
        orcamento = self.repo.buscar_por_id(orcamento_id)
        if not orcamento:
            raise NaoEncontradoError('Orçamento', orcamento_id)
        # self.validar_alteracao(orcamento)

        orcamento.status_orcamento = status
        orcamento_atualizado = self.repo.alterar_status(orcamento_id, status)
        return OrcamentoMapper.entity_to_output_dto(orcamento_atualizado)


class RemoverOrcamentoUseCase:
    def __init__(self, db: Session):
        self.repo = OrcamentoRepository(db)

    # def eh_mecanico_responsavel(self, orcamento: Orcamento) -> bool:
    #     return (
    #         orcamento.funcionario_id == self.funcionario_logado.funcionario_id
    #     )

    def validar_remocao(self, orcamento: Orcamento) -> None:
        # if not self.eh_mecanico_responsavel(orcamento):
        #     raise ApenasMecanicoResponsavel
        if orcamento.status_orcamento == StatusOrcamento.APROVADO:
            raise ValueError(
                'Não é possível remover um orçamento que já foi aprovado.'
            )
        if orcamento.servicos or orcamento.pecas:
            raise ValueError(
                'Não é possível remover um orçamento que possui serviços ou peças vinculados.'
            )

    def executar(self, orcamento_id: int) -> None:
        orcamento = self.repo.buscar_por_id(orcamento_id)
        if not orcamento:
            raise NaoEncontradoError('Orçamento', orcamento_id)
        self.validar_remocao(orcamento)

        self.repo.remover(orcamento_id)
