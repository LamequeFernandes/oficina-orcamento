from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
# from app.core.dependencies import (
#     obter_cliente_logado,
#     obter_funcionario_logado,
#     obter_mecanico_logado,
# )
# from app.modules.usuario.infrastructure.models import ClienteModel, FuncionarioModel
from app.modules.orcamento.application.use_cases import (
    CriarOrcamentoUseCase,
    BuscarOrcamentoUseCase,
    AlterarStatusOrcamentoUseCase,
    RemoverOrcamentoUseCase,
)
from app.modules.orcamento.application.dto import (
    OrcamentoInputDTO,
    OrcamentoOutputDTO,
    OrcamentoAlteraStatusDTO,
)


router = APIRouter()


@router.post(
    '/orcamento',
    response_model=OrcamentoOutputDTO,
    status_code=201,
)
def criar_orcamento(
    dados: OrcamentoInputDTO,
    db: Session = Depends(get_db),
):
    use_case = CriarOrcamentoUseCase(db)
    return use_case.executar(dados)


@router.get(
    '/orcamento/{orcamento_id}',
    response_model=OrcamentoOutputDTO,
)
def buscar_orcamento(
    orcamento_id: int,
    db: Session = Depends(get_db),
):
    use_case = BuscarOrcamentoUseCase(db)
    return use_case.executar(orcamento_id)


@router.patch(
    '/orcamento/{orcamento_id}/status',
    response_model=OrcamentoOutputDTO,
)
def alterar_status_orcamento(
    orcamento_id: int,
    dados: OrcamentoAlteraStatusDTO,
    db: Session = Depends(get_db),
):
    use_case = AlterarStatusOrcamentoUseCase(db)
    return use_case.executar(orcamento_id, dados.status_orcamento)


@router.delete('/orcamento/{orcamento_id}', status_code=204)
def remover_orcamento(
    orcamento_id: int,
    db: Session = Depends(get_db),
):
    use_case = RemoverOrcamentoUseCase(db)
    use_case.executar(orcamento_id)
