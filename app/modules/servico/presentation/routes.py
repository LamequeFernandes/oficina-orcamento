from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
# from app.core.dependencies import obter_funcionario_logado
from app.modules.servico.application.use_cases import (
    CriarServicoUseCase,
    ConsultarServicoUseCase,
    AlterarServicoUseCase,
    RemoverServicoUseCase,
    CriarTipoServicoUseCase,
    ConsultarTipoServicoUseCase,
    ListarTipoServicoUseCase,
    VinculoServicoOrcamentoUseCase,
)
from app.modules.servico.application.dto import (
    TipoServicoInputDTO,
    TipoServicoOutDTO,
    ServicoInputDTO,
    ServicoOutDTO,
)


router = APIRouter()


@router.get('/tipo-servico', response_model=list[TipoServicoOutDTO])
def listar_tipo_servico(
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = ListarTipoServicoUseCase(db)
    return use_case.execute()


@router.post('/', response_model=ServicoOutDTO, status_code=201)
def criar_servico(
    dados: ServicoInputDTO,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = CriarServicoUseCase(db)
    return use_case.execute(dados)


@router.get('/{servico_id}', response_model=ServicoOutDTO)
def consultar_servico(
    servico_id: int,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = ConsultarServicoUseCase(db)
    return use_case.execute(servico_id)


@router.put('/{servico_id}', response_model=ServicoOutDTO)
def alterar_servico(
    servico_id: int,
    dados: ServicoInputDTO,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = AlterarServicoUseCase(db)
    return use_case.execute(servico_id, dados)


@router.patch('/{servico_id}/desvincular', response_model=ServicoOutDTO)
def desvincular_servico(
    servico_id: int,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = VinculoServicoOrcamentoUseCase(db)
    return use_case.execute_desvincular(servico_id)


@router.patch(
    '/{servico_id}/vincular/{orcamento_id}', response_model=ServicoOutDTO
)
def vincular_servico(
    servico_id: int,
    orcamento_id: int,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = VinculoServicoOrcamentoUseCase(db)
    return use_case.execute_vincular(servico_id, orcamento_id)


@router.delete('/{servico_id}', response_model=None, status_code=204)
def remover_servico(
    servico_id: int,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = RemoverServicoUseCase(db)
    use_case.execute(servico_id)


@router.post(
    '/tipo-servico', response_model=TipoServicoOutDTO, status_code=201
)
def criar_tipo_servico(
    dados: TipoServicoInputDTO,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = CriarTipoServicoUseCase(db)
    return use_case.execute(dados)


@router.get(
    '/tipo-servico/{tipo_servico_id}', response_model=TipoServicoOutDTO
)
def consultar_tipo_servico(
    tipo_servico_id: int,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = ConsultarTipoServicoUseCase(db)
    return use_case.execute(tipo_servico_id)
