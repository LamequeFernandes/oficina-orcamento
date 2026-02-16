from app.modules.peca.domain.entities import TipoPeca, Peca
from app.modules.peca.application.dto import TipoPecaOutDTO, PecaOutDTO
from app.modules.peca.infrastructure.models import TipoPecaModel, PecaModel


class TipoPecaMapper:
    @staticmethod
    def entity_to_model(tipo_peca: TipoPeca) -> TipoPecaModel:
        return TipoPecaModel(
            tipo_peca_id=tipo_peca.tipo_peca_id,
            nome_peca=tipo_peca.nome_peca,
            peca_critica=tipo_peca.peca_critica,
        )

    @staticmethod
    def model_to_entity(tipo_peca_model: TipoPecaModel) -> TipoPeca:
        return TipoPeca(
            tipo_peca_id=tipo_peca_model.tipo_peca_id,  # type: ignore
            nome_peca=tipo_peca_model.nome_peca,  # type: ignore
            peca_critica=tipo_peca_model.peca_critica,  # type: ignore
        )

    @staticmethod
    def entity_to_output_dto(tipo_peca: TipoPeca) -> TipoPecaOutDTO:
        return TipoPecaOutDTO(
            tipo_peca_id=tipo_peca.tipo_peca_id,
            nome_peca=tipo_peca.nome_peca,
            peca_critica=tipo_peca.peca_critica,
        )


class PecaMapper:
    @staticmethod
    def entity_to_model(peca: Peca) -> PecaModel:
        return PecaModel(
            peca_id=peca.peca_id,
            tipo_peca_id=peca.tipo_peca_id,
            valor_peca=peca.valor_peca,
            marca=peca.marca,
            orcamento_id=peca.orcamento_id,
        )

    @staticmethod
    def model_to_entity(peca_model: PecaModel) -> Peca:
        return Peca(
            peca_id=peca_model.peca_id,  # type: ignore
            tipo_peca_id=peca_model.tipo_peca_id,  # type: ignore
            valor_peca=peca_model.valor_peca,  # type: ignore
            marca=peca_model.marca,  # type: ignore
            orcamento_id=peca_model.orcamento_id,  # type: ignore
            tipo_peca=TipoPecaMapper.model_to_entity(peca_model.tipo_peca),  # type: ignore
        )

    @staticmethod
    def entity_to_output_dto(peca: Peca) -> PecaOutDTO:
        return PecaOutDTO(
            peca_id=peca.peca_id,
            tipo_peca=TipoPecaMapper.entity_to_output_dto(peca.tipo_peca),  # type: ignore
            valor_peca=peca.valor_peca,
            marca=peca.marca,
            orcamento_id=peca.orcamento_id,
        )
