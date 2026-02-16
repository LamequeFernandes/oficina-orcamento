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

    def remover(self, orcamento_id: int) -> None:
        orcamento_model = (
            self.db.query(OrcamentoModel).filter_by(id=orcamento_id).first()
        )
        self.db.delete(orcamento_model)  # type: ignore
        self.db.commit()
