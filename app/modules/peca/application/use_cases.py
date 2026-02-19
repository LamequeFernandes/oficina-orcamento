from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import (
    ApenasMecanicoResponsavel,
    NaoEncontradoError,
    ValorDuplicadoError,
)
from app.core.utils import obter_valor_e_key_duplicado_integrity_error

from app.modules.orcamento.infrastructure.models import OrcamentoModel
from app.modules.peca.application.dto import (
    PecaInputDTO,
    PecaOutDTO,
    TipoPecaInputDTO,
    TipoPecaOutDTO,
)
from app.modules.peca.infrastructure.mapper import PecaMapper, TipoPecaMapper

from app.modules.peca.domain.entities import Peca, TipoPeca
from app.modules.peca.infrastructure.models import PecaModel
from app.modules.peca.infrastructure.repositories import (
    PecaRepository,
    TipoPecaRepository,
)
# from app.modules.usuario.infrastructure.models import UsuarioModel


class CriarPecaUseCase:
    def __init__(self, db: Session):
        self.repo = PecaRepository(db)

    def execute(self, dados: PecaInputDTO) -> PecaOutDTO:
        peca = Peca(
            peca_id=None,
            tipo_peca_id=dados.tipo_peca_id,
            valor_peca=dados.valor_peca,
            marca=dados.marca,
            orcamento_id=dados.orcamento_id,
        )
        try:
            peca_salva = self.repo.salvar(peca)
        except IntegrityError as e:
            (
                valor_duplicado,
                chave,
            ) = obter_valor_e_key_duplicado_integrity_error(e)
            raise ValorDuplicadoError(valor_duplicado, chave)
        return PecaMapper.entity_to_output_dto(peca_salva)


class ConsultarPecaUseCase:
    def __init__(self, db: Session):
        self.repo = PecaRepository(db)

    def execute(self, peca_id: int) -> PecaOutDTO | None:
        peca = self.repo.buscar_por_id(peca_id)
        if not peca:
            raise NaoEncontradoError('Peça', peca_id)
        return PecaMapper.entity_to_output_dto(peca)


class ListarPecasUseCase:
    def __init__(self, db: Session):
        self.repo = PecaRepository(db)

    def execute(self) -> list[PecaOutDTO]:
        pecas = self.repo.listar()
        return [PecaMapper.entity_to_output_dto(peca) for peca in pecas]


class AlterarPecaUseCase:
    def __init__(self, db: Session):
        self.repo = PecaRepository(db)

    def execute(self, peca_id: int, dados: PecaInputDTO) -> PecaOutDTO:
        peca = self.repo.buscar_por_id(peca_id)
        if not peca:
            raise NaoEncontradoError('Peça', peca_id)

        peca.tipo_peca_id = dados.tipo_peca_id
        peca.valor_peca = dados.valor_peca
        peca.marca = dados.marca
        peca.orcamento_id = dados.orcamento_id

        try:
            peca_alterada = self.repo.alterar(peca)
        except IntegrityError as e:
            (
                valor_duplicado,
                chave,
            ) = obter_valor_e_key_duplicado_integrity_error(e)
            raise ValorDuplicadoError(valor_duplicado, chave)
        return PecaMapper.entity_to_output_dto(peca_alterada)


class CriarTipoPecaUseCase:
    def __init__(self, db: Session):
        self.repo = TipoPecaRepository(db)

    def execute(self, dados: TipoPecaInputDTO) -> TipoPecaOutDTO:
        tipo_peca = TipoPeca(
            tipo_peca_id=None,
            nome_peca=dados.nome_peca,
            peca_critica=dados.peca_critica,
        )
        tipo_peca_salva = self.repo.salvar(tipo_peca)
        return TipoPecaMapper.entity_to_output_dto(tipo_peca_salva)


class ConsultarTipoPecaUseCase:
    def __init__(self, db: Session):
        self.repo = TipoPecaRepository(db)

    def execute(self, tipo_peca_id: int) -> TipoPecaOutDTO | None:
        tipo_peca = self.repo.buscar_por_id(tipo_peca_id)
        if not tipo_peca:
            raise NaoEncontradoError('Tipo de Peça', tipo_peca_id)
        return TipoPecaMapper.entity_to_output_dto(tipo_peca)


class ListarTipoPecasUseCase:
    def __init__(self, db: Session):
        self.repo = TipoPecaRepository(db)

    def execute(self) -> list[TipoPecaOutDTO]:
        tipo_pecas = self.repo.listar()
        return [
            TipoPecaMapper.entity_to_output_dto(tipo_peca)
            for tipo_peca in tipo_pecas
        ]


class VinculoPecaOrcamentoUseCase:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PecaRepository(db)
        # self.funcionario_logado = funcionario_logado

    def valida_status(self, orcamento_model: OrcamentoModel):
        if (
            orcamento_model.status_orcamento != 'AGUARDANDO_APROVACAO'
        ):   # type: ignore
            raise ValueError(
                "Status do orçamento não permite essa ação. Tal alteração só pode ser realizada se o status por: 'AGUARDANDO APROVACAO'."
            )

    def valida_permissao(self, peca_model: PecaModel):
        if peca_model.orcamento_id:   # type: ignore
            if (
                peca_model.orcamento.status_orcamento != 'AGUARDANDO_APROVACAO'
            ):   # type: ignore
                raise ValueError(
                    "Status do orçamento não permite essa ação. Tal alteração só pode ser realizada se o status por: 'AGUARDANDO APROVACAO'."
                )

    def execute_desvincular(self, peca_id: int) -> PecaOutDTO:
        peca = (
            self.db.query(PecaModel)
            .filter(
                PecaModel.peca_id == peca_id,
            )
            .first()
        )
        if not peca:
            raise NaoEncontradoError('Peça', peca_id)
        self.valida_permissao(peca)

        peca = self.repo.desvincular_de_orcamento(peca_id)
        return PecaMapper.entity_to_output_dto(peca)

    def execute_vincular(self, peca_id: int, orcamento_id: int) -> PecaOutDTO:
        peca = (
            self.db.query(PecaModel)
            .filter(
                PecaModel.peca_id == peca_id,
            )
            .first()
        )
        if not peca:
            raise NaoEncontradoError('Peça', peca_id)
        self.valida_permissao(peca)

        orcamento = (
            self.db.query(OrcamentoModel)
            .filter(
                OrcamentoModel.orcamento_id == orcamento_id,
            )
            .first()
        )
        if not orcamento:
            raise NaoEncontradoError('Orçamento', orcamento_id)
        self.valida_status(orcamento)

        peca = self.repo.vincular_a_orcamento(peca_id, orcamento_id)
        return PecaMapper.entity_to_output_dto(peca)
