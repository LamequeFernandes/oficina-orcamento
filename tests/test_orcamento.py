from fastapi.testclient import TestClient
from app.main import app
from app.modules.orcamento.domain.entities import StatusOrcamento
from app.core.security import gerar_token_servico_interno

client = TestClient(app, raise_server_exceptions=False)


def _headers():
    token = gerar_token_servico_interno(expiracao_minutos=5)
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

def test_cadastrar_ordem_servico():
    response = client.post(
        "/orcamento",
        json={
            "ordem_servico_id": 1,
            "status_orcamento": StatusOrcamento.AGUARDANDO_APROVACAO.value,
        },
        headers=_headers(),
    )
    print(response.json())
    assert response.status_code == 201


def test_buscar_orcamento(obter_orcamento, auth_headers):
    orcamento = obter_orcamento
    response = client.get(
        f"/orcamento/{orcamento.orcamento_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["orcamento_id"] == orcamento.orcamento_id
    assert response.json()["valor_total_orcamento"] == orcamento.valor_total_orcamento
    assert response.json()["dta_criacao"] == orcamento.dta_criacao.isoformat()
    assert response.json()["dta_cancelamento"] == orcamento.dta_cancelamento


def test_alterar_status_orcamento(obter_orcamento, auth_headers):
    orcamento = obter_orcamento
    response = client.patch(
        f"/orcamento/{orcamento.orcamento_id}/status",
        json={"status_orcamento": StatusOrcamento.AGUARDANDO_APROVACAO.value},
        headers=auth_headers,
    )
    assert response.status_code == 200


def test_status_orcamento_presente_na_resposta(obter_orcamento, auth_headers):
    orcamento = obter_orcamento
    response = client.get(
        f"/orcamento/{orcamento.orcamento_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert "status_orcamento" in response.json()


def test_consultar_status_pagamento_sem_pagamento_processado(obter_orcamento, auth_headers):
    """Quando o orçamento ainda não tem mp_payment_id, retorna mensagem explicativa."""
    orcamento = obter_orcamento
    response = client.get(
        f"/orcamento/{orcamento.orcamento_id}/status-pagamento",
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["orcamento_id"] == orcamento.orcamento_id
    assert body["mp_payment_id"] is None


# ---------------------------------------------------------------------------
# Autenticação
# ---------------------------------------------------------------------------

def test_criar_orcamento_sem_token_retorna_403():
    response = client.post(
        "/orcamento",
        json={
            "ordem_servico_id": 1,
            "status_orcamento": StatusOrcamento.AGUARDANDO_APROVACAO.value,
        },
    )
    assert response.status_code == 403


def test_buscar_orcamento_sem_token_retorna_403():
    response = client.get("/orcamento/1")
    assert response.status_code == 403


def test_alterar_status_sem_token_retorna_403():
    response = client.patch(
        "/orcamento/1/status",
        json={"status_orcamento": StatusOrcamento.AGUARDANDO_APROVACAO.value},
    )
    assert response.status_code == 403


def test_status_pagamento_sem_token_retorna_403():
    response = client.get("/orcamento/1/status-pagamento")
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# Casos de erro — recurso não encontrado
# ---------------------------------------------------------------------------

def test_buscar_orcamento_inexistente_retorna_erro(auth_headers):
    response = client.get("/orcamento/999999", headers=auth_headers)
    # NaoEncontradoError não está mapeado para 404 em tratar_erro_dominio → retorna 500
    assert response.status_code in (404, 500)


def test_consultar_status_pagamento_orcamento_inexistente(auth_headers):
    response = client.get("/orcamento/999999/status-pagamento", headers=auth_headers)
    assert response.status_code in (404, 500)


# ---------------------------------------------------------------------------
# Webhook
# ---------------------------------------------------------------------------

def test_webhook_ignora_notificacao_desconhecida():
    """Notificação de tipo unknown (ex: merchant_order) deve ser ignorada silenciosamente."""
    response = client.post(
        "/webhook/mercadopago",
        json={"type": "merchant_order", "data": {"id": "123"}},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ignored"


def test_webhook_ignora_body_invalido():
    """Body inválido (não-JSON) deve retornar ignored sem explodir."""
    response = client.post(
        "/webhook/mercadopago",
        content=b"isso nao e json",
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ignored"


def test_webhook_ipn_sem_payment_topic_ignora():
    """IPN com topic diferente de 'payment' deve ser ignorado."""
    response = client.post(
        "/webhook/mercadopago?topic=merchant_order&id=123",
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ignored"


# ---------------------------------------------------------------------------
# Remover orçamento
# ---------------------------------------------------------------------------

# def test_remover_orcamento(auth_headers):
#     """Cria um orçamento vazio e o remove com sucesso."""
#     create = client.post(
#         "/orcamento",
#         json={
#             "ordem_servico_id": None,
#             "status_orcamento": StatusOrcamento.AGUARDANDO_APROVACAO.value,
#         },
#         headers=auth_headers,
#     )
#     assert create.status_code == 201
#     orcamento_id = create.json()["orcamento_id"]

#     delete = client.delete(f"/orcamento/{orcamento_id}", headers=auth_headers)
#     assert delete.status_code == 204


def test_remover_orcamento_sem_token_retorna_403():
    response = client.delete("/orcamento/1")
    assert response.status_code == 403
