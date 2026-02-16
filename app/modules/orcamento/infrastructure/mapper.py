from app.modules.peca.infrastructure.mapper import PecaMapper
from app.modules.servico.infrastructure.mapper import ServicoMapper
# from app.modules.usuario.domain.entities import Funcionario
# from app.modules.usuario.infrastructure.mapper import FuncionarioMapper
from app.modules.orcamento.domain.entities import Orcamento
from app.modules.orcamento.application.dto import OrcamentoOutputDTO
from app.modules.orcamento.infrastructure.models import OrcamentoModel


class OrcamentoMapper:
    @staticmethod
    def entity_to_model(orcamento: Orcamento) -> OrcamentoModel:
        return OrcamentoModel(
            orcamento_id=orcamento.orcamento_id,
            # funcionario_id=orcamento.funcionario_id,
            status_orcamento=orcamento.status_orcamento,
            ordem_servico_id=orcamento.ordem_servico_id,
            dta_criacao=orcamento.dta_criacao,
            dta_cancelamento=orcamento.dta_cancelamento,
        )

    @staticmethod
    def model_to_entity(orcamento_model: OrcamentoModel) -> Orcamento:
        return Orcamento(
            orcamento_id=orcamento_model.orcamento_id,  # type: ignore
            # funcionario_id=orcamento_model.funcionario_id,  # type: ignore
            status_orcamento=orcamento_model.status_orcamento,  # type: ignore
            ordem_servico_id=orcamento_model.ordem_servico_id,  # type: ignore
            dta_criacao=orcamento_model.dta_criacao,  # type: ignore
            dta_cancelamento=orcamento_model.dta_cancelamento,  # type: ignore
            # funcionario=Funcionario(
            #     funcionario_id=orcamento_model.funcionario.funcionario_id,  # type: ignore
            #     usuario=orcamento_model.funcionario.usuario,  # type: ignore
            #     matricula=orcamento_model.funcionario.matricula,  # type: ignore
            #     tipo=orcamento_model.funcionario.tipo_funcionario,  # type: ignore
            #     cpf=orcamento_model.funcionario.cpf,  # type: ignore
            # ),
            servicos=[
                ServicoMapper.model_to_entity(servico_model)
                for servico_model in orcamento_model.servicos
            ],
            pecas=[
                PecaMapper.model_to_entity(peca_model)
                for peca_model in orcamento_model.pecas
            ],
        )

    @staticmethod
    def entity_to_output_dto(orcamento: Orcamento) -> OrcamentoOutputDTO:
        return OrcamentoOutputDTO(
            orcamento_id=orcamento.orcamento_id,  # type: ignore
            # status_orcamento=orcamento.status_orcamento,
            valor_total_orcamento=orcamento.valor_total_orcamento,  # type: ignore
            # funcionario_id=orcamento.funcionario_id,
            dta_criacao=orcamento.dta_criacao,
            # funcionario_responsavel=FuncionarioMapper.entity_to_output_dto(orcamento.funcionario),  # type: ignore
            servicos_inclusos=[
                ServicoMapper.entity_to_output_dto(servico)
                for servico in orcamento.servicos
            ],
            pecas_necessarias=[
                PecaMapper.entity_to_output_dto(peca)
                for peca in orcamento.pecas
            ],
            dta_cancelamento=orcamento.dta_cancelamento,
        )
