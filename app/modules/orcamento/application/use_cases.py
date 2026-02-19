from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    ApenasMecanicoResponsavel,
    NaoEncontradoError,
    ValorDuplicadoError,
)
from app.core.utils import notificar_ordem_servico_paga, obter_valor_e_key_duplicado_integrity_error
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
from app.core.utils import (
    gerar_checkout_preference_mercado_pago,
    verificar_pagamento_mercado_pago,
    notificar_ordem_servico_paga,
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

    def validar_alteracao(self, orcamento: Orcamento) -> None:
        # if not self.eh_mecanico_responsavel(orcamento):
        #     raise ApenasMecanicoResponsavel
        # if not self.eh_cliente_dono_ordem_servico(orcamento):
        #     raise ValueError(
        #         'Apenas o cliente dono da ordem de serviço pode alterar o status do orçamento.'
        #     )

        # if orcamento.status_orcamento == StatusOrcamento.APROVADO:
        #     raise ValueError(
        #         'Não é possível alterar o status de um orçamento que já foi aprovado.'
        #     )
        pass

    def executar(
        self, orcamento_id: int, status: StatusOrcamento
    ) -> OrcamentoOutputDTO:
        orcamento = self.repo.buscar_por_id(orcamento_id)
        if not orcamento:
            raise NaoEncontradoError('Orçamento', orcamento_id)
        # self.validar_alteracao(orcamento)

        orcamento.status_orcamento = status

        if status == StatusOrcamento.APROVADO:
            listar_servicos = orcamento.servicos
            listar_pecas = orcamento.pecas

            response_date_mp = gerar_checkout_preference_mercado_pago(
                orcamento_id, listar_servicos, listar_pecas
            )
            self.repo.atualizar_dados_pagamento(
                orcamento_id,
                url_pagamento=response_date_mp.get("init_point"),
                preference_id=response_date_mp.get("preference_id"),
            )

        orcamento_atualizado = self.repo.alterar_status(orcamento_id, status)
        return OrcamentoMapper.entity_to_output_dto(orcamento_atualizado)


class ProcessarWebhookMercadoPagoUseCase:
    """Processa notificações IPN/Webhooks enviadas pelo Mercado Pago."""

    def __init__(self, db: Session):
        self.repo = OrcamentoRepository(db)

    def executar(self, payment_id: str) -> OrcamentoOutputDTO | None:
        """Consulta o pagamento na API do MP e, se aprovado, marca o orçamento como PAGO."""
        dados_pagamento = verificar_pagamento_mercado_pago(payment_id)

        mp_status: str = dados_pagamento.get("status", "")
        external_reference: str | None = dados_pagamento.get("external_reference")

        if not external_reference:
            return None

        orcamento_id = int(external_reference)
        orcamento = self.repo.buscar_por_id(orcamento_id)
        if not orcamento:
            return None

        # Só atualiza se o pagamento foi aprovado e o orçamento ainda não está pago
        if mp_status == "approved" and orcamento.status_orcamento != StatusOrcamento.PAGO:
            orcamento_atualizado = self.repo.marcar_como_pago(orcamento_id, payment_id)

            # realizar chamada para o microsserviço de ordem de serviço, para alterar o status da ordem de serviço vinculada
            if orcamento_atualizado.ordem_servico_id:
                notificar_ordem_servico_paga(orcamento_atualizado.ordem_servico_id)                  
            return OrcamentoMapper.entity_to_output_dto(orcamento_atualizado)
        return OrcamentoMapper.entity_to_output_dto(orcamento)


class ConsultarStatusPagamentoUseCase:
    """Consulta o status de pagamento de um orçamento diretamente na API do Mercado Pago."""

    def __init__(self, db: Session):
        self.repo = OrcamentoRepository(db)

    def executar(self, orcamento_id: int) -> dict:
        orcamento = self.repo.buscar_por_id(orcamento_id)
        if not orcamento:
            raise NaoEncontradoError('Orçamento', orcamento_id)

        # Se já temos o payment_id armazenado, consultamos diretamente
        if orcamento.mp_payment_id:
            dados = verificar_pagamento_mercado_pago(orcamento.mp_payment_id)
            return {
                "orcamento_id": orcamento_id,
                "status_orcamento": orcamento.status_orcamento,
                "mp_payment_id": orcamento.mp_payment_id,
                "mp_status": dados.get("status"),
                "mp_status_detail": dados.get("status_detail"),
                "mp_payment_method": dados.get("payment_method_id"),
                "mp_payer_email": dados.get("payer", {}).get("email"),
                "valor_pago": dados.get("transaction_amount"),
            }

        # Caso ainda não tenhamos o payment_id, retornamos o status atual
        return {
            "orcamento_id": orcamento_id,
            "status_orcamento": orcamento.status_orcamento,
            "mp_payment_id": None,
            "mp_status": None,
            "mensagem": "Pagamento ainda não foi processado ou webhook não recebido.",
            "url_pagamento": orcamento.url_pagamento,
        }


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
