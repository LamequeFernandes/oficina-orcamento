from sqlalchemy.orm import Session
from app.core.exceptions import NaoEncontradoError, VeiculoNotFoundError
from app.modules.orcamento.domain.entities import Orcamento, StatusOrcamento
from app.modules.orcamento.infrastructure.mapper import OrcamentoMapper
from app.modules.orcamento.infrastructure.models import OrcamentoModel
from app.modules.orcamento.application.interfaces import (
    OrcamentoRepositoryInterface,
)


class OrcamentoRepository(OrcamentoRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, orcamento: Orcamento) -> Orcamento:
        orcamento_model = OrcamentoMapper.entity_to_model(orcamento)
        self.db.add(orcamento_model)
        self.db.commit()
        self.db.refresh(orcamento_model)
        return OrcamentoMapper.model_to_entity(orcamento_model)

    def buscar_por_id(self, orcamento_id: int) -> Orcamento | None:
        orcamento_model = (
            self.db.query(OrcamentoModel).filter_by(orcamento_id=orcamento_id).first()
        )
        return (
            OrcamentoMapper.model_to_entity(orcamento_model)
            if orcamento_model
            else None
        )

    def buscar_por_preference_id(self, preference_id: str) -> Orcamento | None:
        orcamento_model = (
            self.db.query(OrcamentoModel)
            .filter_by(preference_id=preference_id)
            .first()
        )
        return (
            OrcamentoMapper.model_to_entity(orcamento_model)
            if orcamento_model
            else None
        )

    def alterar_status(
        self, orcamento_id: int, novo_status: StatusOrcamento
    ) -> Orcamento:
        orcamento_model = (
            self.db.query(OrcamentoModel).filter_by(orcamento_id=orcamento_id).first()
        )
        orcamento_model.status_orcamento = novo_status  # type: ignore
        self.db.commit()
        self.db.refresh(orcamento_model)
        return OrcamentoMapper.model_to_entity(orcamento_model)

    def atualizar_dados_pagamento(
        self,
        orcamento_id: int,
        url_pagamento: str | None,
        preference_id: str | None,
    ) -> None:
        self.db.query(OrcamentoModel).filter_by(orcamento_id=orcamento_id).update(
            {
                OrcamentoModel.url_pagamento: url_pagamento,
                OrcamentoModel.preference_id: preference_id,
            }
        )
        self.db.commit()

    def marcar_como_pago(
        self,
        orcamento_id: int,
        mp_payment_id: str,
    ) -> Orcamento:
        orcamento_model = (
            self.db.query(OrcamentoModel).filter_by(orcamento_id=orcamento_id).first()
        )
        orcamento_model.status_orcamento = StatusOrcamento.PAGO  # type: ignore
        orcamento_model.mp_payment_id = mp_payment_id  # type: ignore
        self.db.commit()
        self.db.refresh(orcamento_model)
        return OrcamentoMapper.model_to_entity(orcamento_model)

    def remover(self, orcamento_id: int) -> None:
        orcamento_model = (
            self.db.query(OrcamentoModel).filter_by(id=orcamento_id).first()
        )
        self.db.delete(orcamento_model)  # type: ignore
        self.db.commit()
