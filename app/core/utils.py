from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import requests

import re
import logging

from app.core.config import settings
from app.modules.peca.domain.entities import Peca
from app.modules.servico.domain.entities import Servico

logger = logging.getLogger(__name__)


def obter_valor_e_key_duplicado_integrity_error(e: IntegrityError):
    """
    Extrai o valor duplicado de uma exceção IntegrityError.
    """
    msg = str(e.orig)

    match = re.search(r"Duplicate entry '(.+?)' for key '(.+?)'", msg)

    if not match:
        raise e
    valor_duplicado = match.group(1)
    chave = match.group(2).split('.')[-1]

    return valor_duplicado, chave


def gerar_checkout_preference_mercado_pago(orcamento_id: int, listar_servicos: list[Servico], listar_pecas: list[Peca]):
    if not settings.MP_ACCESS_TOKEN:
        raise HTTPException(status_code=500, detail="settings. não configurado")

    lista_items = []

    for servico in listar_servicos:
        nome = servico.tipo_servico.nome_servico if servico.tipo_servico else f"Serviço #{servico.servico_id}"
        item = {
            "title": f"Serviço: {nome}",
            "quantity": 1,
            "unit_price": float(servico.valor_servico),
            "currency_id": "BRL",
        }
        lista_items.append(item)

    for peca in listar_pecas:
        nome = peca.tipo_peca.nome_peca if peca.tipo_peca else f"Peça #{peca.peca_id}"
        item = {
            "title": f"Peça: {nome}",
            "quantity": 1,
            "unit_price": float(peca.valor_peca),
            "currency_id": "BRL",
        }
        lista_items.append(item)

    payload = {
        "items": lista_items,
        "external_reference": str(orcamento_id),  # linka o pagamento ao seu orçamento
        "back_urls": {
            "success": settings.MP_SUCCESS_URL,
            "failure": settings.MP_FAILURE_URL,
            "pending": settings.MP_PENDING_URL,
        },
        "notification_url": settings.MP_NOTIFICATION_URL,  # webhook
        "auto_return": "approved",
    }

    r = requests.post(
        f"{settings.MP_API}/checkout/preferences",
        headers={
            "Authorization": f"Bearer {settings.MP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=20,
    )

    if r.status_code >= 400:
        raise HTTPException(status_code=502, detail={"mp_status": r.status_code, "mp_body": r.text})

    data = r.json()

    # 2) Persistir no seu DB: preference_id, status=PENDING, orcamento_id, etc.
    # repo.save_payment(orcamento_id, data["id"], "PENDING")

    return {
        "orcamento_id": orcamento_id,
        "preference_id": data["id"],
        "init_point": data.get("init_point"),  # URL do checkout
    }


def notificar_ordem_servico_paga(ordem_servico_id: int):
    """
    Realiza uma chamada HTTP para o microsserviço de ordem de serviço, informando o novo status da ordem de serviço vinculada ao orçamento.
    """
    if not ordem_servico_id:
        return

    from app.core.security import gerar_token_servico_interno
    token = gerar_token_servico_interno()

    try:
        r = requests.patch(
            f"{settings.URL_API_OS}/veiculos/1/ordens_servico/{ordem_servico_id}/status",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={"status": "EM_EXECUCAO"},
            timeout=10,
        )
        return r.status_code, r.text
    except requests.RequestException as e:
        # Logar o erro, mas não falhar o processo principal do orçamento
        logger.error(f"Erro ao chamar microsserviço de ordem de serviço: {e}")


def verificar_pagamento_mercado_pago(payment_id: str) -> dict:
    """
    Consulta os detalhes de um pagamento na API do Mercado Pago.

    Retorna os dados do pagamento: status, external_reference, valor, etc.
    Possíveis valores de 'status': pending, approved, authorized, in_process,
    in_mediation, rejected, cancelled, refunded, charged_back.
    """
    if not settings.MP_ACCESS_TOKEN:
        raise HTTPException(status_code=500, detail="MP_ACCESS_TOKEN não configurado")

    r = requests.get(
        f"{settings.MP_API}/v1/payments/{payment_id}",
        headers={
            "Authorization": f"Bearer {settings.MP_ACCESS_TOKEN}",
        },
        timeout=20,
    )

    if r.status_code == 404:
        raise HTTPException(status_code=404, detail=f"Pagamento {payment_id} não encontrado no Mercado Pago")

    if r.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail={"mp_status": r.status_code, "mp_body": r.text},
        )

    return r.json()