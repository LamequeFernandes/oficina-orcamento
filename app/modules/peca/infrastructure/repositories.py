from sqlalchemy.orm import Session
from app.core.exceptions import NaoEncontradoError
from app.modules.peca.domain.entities import Peca, TipoPeca
from app.modules.peca.infrastructure.mapper import PecaMapper, TipoPecaMapper
from app.modules.peca.infrastructure.models import PecaModel, TipoPecaModel
from app.modules.peca.application.interfaces import (
    PecaRepositoryInterface,
    TipoPecaRepositoryInterface,
)


class PecaRepository(PecaRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, peca: Peca) -> Peca:
        peca_model = PecaMapper.entity_to_model(peca)
        self.db.add(peca_model)
        self.db.commit()
        self.db.refresh(peca_model)
        return PecaMapper.model_to_entity(peca_model)

    def buscar_por_id(self, peca_id: int) -> Peca | None:
        peca_model = (
            self.db.query(PecaModel)
            .filter(PecaModel.peca_id == peca_id)
            .first()
        )
        return PecaMapper.model_to_entity(peca_model) if peca_model else None

    def alterar(self, peca: Peca) -> Peca:
        peca_model = self.db.query(PecaModel).filter(PecaModel.peca_id == peca.peca_id).first()
        self.db.merge(peca_model)
        self.db.commit()
        self.db.refresh(peca_model)
        return PecaMapper.model_to_entity(peca_model)

    def listar(self) -> list[Peca]:
        peca_models = self.db.query(PecaModel).all()
        return [PecaMapper.model_to_entity(model) for model in peca_models]

    def vincular_a_orcamento(self, peca_id: int, orcamento_id: int) -> Peca:
        peca = self.buscar_por_id(peca_id)
        if not peca:
            raise NaoEncontradoError('Peça', peca_id)
        peca.orcamento_id = orcamento_id
        self.db.commit()
        return peca

    def desvincular_de_orcamento(self, peca_id: int) -> Peca:
        peca = self.buscar_por_id(peca_id)
        if not peca:
            raise NaoEncontradoError('Peça', peca_id)
        peca.orcamento_id = None
        self.db.commit()
        return peca


class TipoPecaRepository(TipoPecaRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, tipo_peca: TipoPeca) -> TipoPeca:
        tipo_peca_model = TipoPecaMapper.entity_to_model(tipo_peca)
        self.db.add(tipo_peca_model)
        self.db.commit()
        self.db.refresh(tipo_peca_model)
        return TipoPecaMapper.model_to_entity(tipo_peca_model)

    def buscar_por_id(self, tipo_peca_id: int) -> TipoPeca | None:
        tipo_peca_model = (
            self.db.query(TipoPecaModel)
            .filter(TipoPecaModel.tipo_peca_id == tipo_peca_id)
            .first()
        )
        return (
            TipoPecaMapper.model_to_entity(tipo_peca_model)
            if tipo_peca_model
            else None
        )

    def listar(self) -> list[TipoPeca]:
        tipo_peca_models = self.db.query(TipoPecaModel).all()
        return [
            TipoPecaMapper.model_to_entity(model) for model in tipo_peca_models
        ]
