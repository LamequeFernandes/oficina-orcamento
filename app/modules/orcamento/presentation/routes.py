from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.config import settings
# from app.core.dependencies import (
#     obter_cliente_logado,
#     obter_funcionario_logado,
#     obter_mecanico_logado,
# )
# from app.modules.usuario.infrastructure.models import ClienteModel, FuncionarioModel
from app.core.dependencies import obter_id_usuario_logado
from app.modules.orcamento.application.use_cases import (
    CriarOrcamentoUseCase,
    BuscarOrcamentoUseCase,
    AlterarStatusOrcamentoUseCase,
    RemoverOrcamentoUseCase,
    ProcessarWebhookMercadoPagoUseCase,
    ConsultarStatusPagamentoUseCase,
)
from app.modules.orcamento.application.dto import (
    OrcamentoInputDTO,
    OrcamentoOutputDTO,
    OrcamentoAlteraStatusDTO,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    '/orcamento',
    response_model=OrcamentoOutputDTO,
    status_code=201,
)
def criar_orcamento(
    dados: OrcamentoInputDTO,
    db: Session = Depends(get_db),
    usuario_logado_id: int = Depends(obter_id_usuario_logado),
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
    usuario_logado_id: int = Depends(obter_id_usuario_logado),
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
    usuario_logado_id: int = Depends(obter_id_usuario_logado),
):
    use_case = AlterarStatusOrcamentoUseCase(db)
    return use_case.executar(orcamento_id, dados.status_orcamento)


@router.get(
    '/orcamento/{orcamento_id}/status-pagamento',
    summary='Consultar status de pagamento no Mercado Pago',
)
def consultar_status_pagamento(
    orcamento_id: int,
    db: Session = Depends(get_db),
    usuario_logado_id: int = Depends(obter_id_usuario_logado),
):
    """
    Retorna o status atual do pagamento para o orçamento informado.
    Se o webhook já foi recebido e o mp_payment_id foi salvo, consulta
    diretamente a API do Mercado Pago para obter detalhes atualizados.
    """
    use_case = ConsultarStatusPagamentoUseCase(db)
    return use_case.executar(orcamento_id)


@router.post(
    '/webhook/mercadopago',
    status_code=200,
    summary='Webhook de notificações do Mercado Pago',
)
async def webhook_mercado_pago(
    request: Request,
    db: Session = Depends(get_db),
    topic: str | None = Query(default=None),
    id: str | None = Query(default=None, alias='id'),
):
    """
    Endpoint chamado pelo Mercado Pago quando há uma atualização de pagamento.

    Suporta dois formatos:
    - IPN legado: query params `topic=payment&id={payment_id}`
    - Webhooks API v2: corpo JSON com `{ "type": "payment", "data": { "id": "..." } }`
    """
    payment_id: str | None = None

    # Formato IPN legado via query string
    if topic == 'payment' and id:
        payment_id = id
    else:
        # Formato novo: corpo JSON
        try:
            body = await request.json()
            if body.get('type') == 'payment':
                payment_id = str(body['data']['id'])
        except Exception:
            logger.warning('Webhook MP: corpo inválido recebido')

    if not payment_id:
        # Ignorar silenciosamente notificações de outros tipos (ex: merchant_order)
        return {'status': 'ignored'}

    logger.info(f'Webhook MP recebido: payment_id={payment_id}')

    use_case = ProcessarWebhookMercadoPagoUseCase(db)
    use_case.executar(payment_id)

    return {'status': 'ok'}


@router.delete('/orcamento/{orcamento_id}', status_code=204)
def remover_orcamento(
    orcamento_id: int,
    db: Session = Depends(get_db),
    usuario_logado_id: int = Depends(obter_id_usuario_logado),
):
    use_case = RemoverOrcamentoUseCase(db)
    use_case.executar(orcamento_id)

