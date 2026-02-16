from fastapi.testclient import TestClient
from app.main import app
from app.modules.orcamento.domain.entities import StatusOrcamento

client = TestClient(app, raise_server_exceptions=False)


def test_cadastrar_ordem_servico():
    response = client.post(
        f"/orcamento",
        json={
            "ordem_servico_id": 1,
            "status_orcamento": StatusOrcamento.AGUARDANDO_APROVACAO.value
        },
        # headers={
        #     "Authorization": f"Bearer {token_mecanico}"
        # }
    )
    print(response.json())
    assert response.status_code == 201


def test_buscar_orcamento(obter_orcamento):
    orcamento = obter_orcamento
    response = client.get(
        f"/orcamento/{orcamento.orcamento_id}",
        # headers={
        #     "Authorization": f"Bearer {token_mecanico}"
        # }
    )
    assert response.status_code == 200
    assert response.json()["orcamento_id"] == orcamento.orcamento_id
    # assert response.json()["funcionario_id"] == orcamento.funcionario_id
    assert response.json()["valor_total_orcamento"] == orcamento.valor_total_orcamento
    assert response.json()["dta_criacao"] == orcamento.dta_criacao.isoformat()
    assert response.json()["dta_cancelamento"] == orcamento.dta_cancelamento
    # assert response.json()["funcionario_responsavel"]["funcionario_id"] == orcamento.funcionario_responsavel.funcionario_id


def test_alterar_status_orcamento(obter_orcamento):
    orcamento = obter_orcamento
    response = client.patch(
        f"/orcamento/{orcamento.orcamento_id}/status",
        json={
            "status_orcamento": StatusOrcamento.APROVADO.value
        },
        # headers={
        #     "Authorization": f"Bearer {token_cliente}"
        # }
    )
    assert response.status_code == 200
    # assert response.json()["status_orcamento"] == StatusOrcamento.APROVADO.value

# TO DO
# def test_deletar_orcamento(obter_orcamento, obter_mecanico):
#     _, ordem_servico, orcamento = obter_orcamento
#     token_mecanico, _ = obter_mecanico
#     response = client.delete(
#         f"/orcamento/{orcamento.orcamento_id}",
#         headers={
#             "Authorization": f"Bearer {token_mecanico}"
#         }
#     )
#     assert response.status_code == 204
