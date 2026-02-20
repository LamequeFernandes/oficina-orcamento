from sqlalchemy.orm import Session
from app.modules.servico.domain.entities import Servico, TipoServico
from app.modules.servico.infrastructure.mapper import (
    ServicoMapper,
    TipoServicoMapper,
)
from app.modules.servico.infrastructure.models import (
    ServicoModel,
    TipoServicoModel,
)
from app.modules.servico.application.interfaces import (
    ServicoRepositoryInterface,
    TipoServicoRepositoryInterface,
)


class ServicoRepository(ServicoRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, servico: Servico) -> Servico:
        servico_model = ServicoMapper.entity_to_model(servico)
        self.db.add(servico_model)
        self.db.commit()
        self.db.refresh(servico_model)
        return ServicoMapper.model_to_entity(servico_model)

    def buscar_por_id(self, servico_id: int) -> Servico | None:
        servico_model = (
            self.db.query(ServicoModel)
            .filter(ServicoModel.servico_id == servico_id)
            .first()
        )
        return (
            ServicoMapper.model_to_entity(servico_model)
            if servico_model
            else None
        )

    def remover(self, servico_id: int) -> bool:
        servico_model = (
            self.db.query(ServicoModel)
            .filter(ServicoModel.servico_id == servico_id)
            .first()
        )
        if servico_model:
            self.db.delete(servico_model)
            self.db.commit()
            return True
        return False

    def alterar(self, servico: Servico) -> Servico:
        # servico_model = ServicoMapper.entity_to_model(servico)
        servico_model = self.db.query(ServicoModel).filter(ServicoModel.servico_id == servico.servico_id).first()
        
        servico_model.valor_servico = servico.valor_servico # type: ignore
        servico_model.tipo_servico_id = servico.tipo_servico_id # type: ignore
        servico_model.orcamento_id = servico.orcamento_id # type: ignore

        self.db.merge(servico_model)
        self.db.commit()
        return ServicoMapper.model_to_entity(servico_model)

    def vincular_a_orcamento(
        self, servico_id: int, orcamento_id: int
    ) -> Servico:
        servico_model = (
            self.db.query(ServicoModel)
            .filter(ServicoModel.servico_id == servico_id)
            .first()
        )
        servico_model.orcamento_id = orcamento_id   # type: ignore
        self.db.commit()
        self.db.refresh(servico_model)
        return ServicoMapper.model_to_entity(servico_model)

    def desvincular_de_orcamento(self, servico_id: int) -> Servico:
        servico_model = (
            self.db.query(ServicoModel)
            .filter(ServicoModel.servico_id == servico_id)
            .first()
        )
        servico_model.orcamento_id = None   # type: ignore
        self.db.commit()
        self.db.refresh(servico_model)
        return ServicoMapper.model_to_entity(servico_model)


class TipoServicoRepository(TipoServicoRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, tipo_servico: TipoServico) -> TipoServico:
        tipo_servico_model = TipoServicoMapper.entity_to_model(tipo_servico)
        self.db.add(tipo_servico_model)
        self.db.commit()
        self.db.refresh(tipo_servico_model)
        return TipoServicoMapper.model_to_entity(tipo_servico_model)

    def buscar_por_id(self, tipo_servico_id: int) -> TipoServico | None:
        tipo_servico_model = (
            self.db.query(TipoServicoModel)
            .filter(TipoServicoModel.tipo_servico_id == tipo_servico_id)
            .first()
        )
        return (
            TipoServicoMapper.model_to_entity(tipo_servico_model)
            if tipo_servico_model
            else None
        )

    def listar(self) -> list[TipoServico]:
        tipo_servico_models = self.db.query(TipoServicoModel).all()
        return [
            TipoServicoMapper.model_to_entity(model)
            for model in tipo_servico_models
        ]
