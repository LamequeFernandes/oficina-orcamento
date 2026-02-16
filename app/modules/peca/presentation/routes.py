from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
# from app.core.dependencies import obter_funcionario_logado
from app.modules.peca.application.use_cases import (
    CriarPecaUseCase,
    ConsultarPecaUseCase,
    ListarPecasUseCase,
    AlterarPecaUseCase,
    CriarTipoPecaUseCase,
    ConsultarTipoPecaUseCase,
    ListarTipoPecasUseCase,
    VinculoPecaOrcamentoUseCase,
)
from app.modules.peca.application.dto import (
    TipoPecaInputDTO,
    TipoPecaOutDTO,
    PecaInputDTO,
    PecaOutDTO,
)


router = APIRouter()


@router.get('/tipo-peca', response_model=list[TipoPecaOutDTO])
def listar_tipo_pecas(
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = ListarTipoPecasUseCase(db)
    return use_case.execute()


@router.post('/', response_model=PecaOutDTO, status_code=201)
def criar_peca(
    dados: PecaInputDTO,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = CriarPecaUseCase(db)
    return use_case.execute(dados)


@router.get('/{peca_id}', response_model=PecaOutDTO)
def consultar_peca(
    peca_id: int,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = ConsultarPecaUseCase(db)
    return use_case.execute(peca_id)


@router.put('/{peca_id}', response_model=PecaOutDTO)
def alterar_peca(
    peca_id: int,
    dados: PecaInputDTO,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = AlterarPecaUseCase(db)
    return use_case.execute(peca_id, dados)


@router.get('/', response_model=list[PecaOutDTO])
def listar_pecas(
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = ListarPecasUseCase(db)
    return use_case.execute()


@router.patch('/{peca_id}/desvincular', response_model=PecaOutDTO)
def desvincular_peca(
    peca_id: int,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = VinculoPecaOrcamentoUseCase(db)
    return use_case.execute_desvincular(peca_id)


@router.patch('/{peca_id}/vincular/{orcamento_id}', response_model=PecaOutDTO)
def vincular_peca(
    peca_id: int,
    orcamento_id: int,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = VinculoPecaOrcamentoUseCase(db)
    return use_case.execute_vincular(peca_id, orcamento_id)


@router.post('/tipo-peca', response_model=TipoPecaOutDTO, status_code=201)
def criar_tipo_peca(
    dados: TipoPecaInputDTO,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = CriarTipoPecaUseCase(db)
    return use_case.execute(dados)


@router.get('/tipo-peca/{tipo_peca_id}', response_model=TipoPecaOutDTO)
def consultar_tipo_peca(
    tipo_peca_id: int,
    db: Session = Depends(get_db),
    # funcionario=Depends(obter_funcionario_logado),
):
    use_case = ConsultarTipoPecaUseCase(db)
    return use_case.execute(tipo_peca_id)
