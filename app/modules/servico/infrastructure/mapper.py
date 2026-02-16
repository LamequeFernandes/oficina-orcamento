from app.modules.servico.domain.entities import TipoServico, Servico
from app.modules.servico.application.dto import (
    TipoServicoOutDTO,
    ServicoOutDTO,
)
from app.modules.servico.infrastructure.models import (
    TipoServicoModel,
    ServicoModel,
)


class TipoServicoMapper:
    @staticmethod
    def entity_to_model(tipo_servico: TipoServico) -> TipoServicoModel:
        return TipoServicoModel(
            tipo_servico_id=tipo_servico.tipo_servico_id,
            nome_servico=tipo_servico.nome_servico,
            descricao=tipo_servico.descricao,
        )

    @staticmethod
    def model_to_entity(tipo_servico_model: TipoServicoModel) -> TipoServico:
        return TipoServico(
            tipo_servico_id=tipo_servico_model.tipo_servico_id,  # type: ignore
            nome_servico=tipo_servico_model.nome_servico,  # type: ignore
            descricao=tipo_servico_model.descricao,  # type: ignore
        )

    @staticmethod
    def entity_to_output_dto(tipo_servico: TipoServico) -> TipoServicoOutDTO:
        return TipoServicoOutDTO(
            tipo_servico_id=tipo_servico.tipo_servico_id,
            nome_servico=tipo_servico.nome_servico,
            descricao=tipo_servico.descricao,
        )


class ServicoMapper:
    @staticmethod
    def entity_to_model(servico: Servico) -> ServicoModel:
        return ServicoModel(
            servico_id=servico.servico_id,
            tipo_servico_id=servico.tipo_servico_id, 
            valor_servico=servico.valor_servico,
            orcamento_id=servico.orcamento_id,
        )

    @staticmethod
    def model_to_entity(servico_model: ServicoModel) -> Servico:
        return Servico(
            servico_id=servico_model.servico_id,  # type: ignore
            tipo_servico_id=servico_model.tipo_servico_id,  # type: ignore
            valor_servico=servico_model.valor_servico,  # type: ignore
            orcamento_id=servico_model.orcamento_id,  # type: ignore
            tipo_servico=TipoServicoMapper.model_to_entity(servico_model.tipo_servico),  # type: ignore
        )

    @staticmethod
    def entity_to_output_dto(servico: Servico) -> ServicoOutDTO:
        return ServicoOutDTO(
            servico_id=servico.servico_id,
            tipo_servico=TipoServicoMapper.entity_to_output_dto(
                servico.tipo_servico  # type: ignore
            ),
            valor_servico=servico.valor_servico,
            orcamento_id=servico.orcamento_id,
        )
