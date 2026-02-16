from fastapi.testclient import TestClient
from app.main import app
from app.modules.orcamento.domain.entities import StatusOrcamento


client = TestClient(app, raise_server_exceptions=False)


def test_lista_tipo_servico():
    response = client.get(
        "/servicos/tipo-servico",
        # headers={
        #     "Authorization": f"Bearer {token_funcionario}"
        # }
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_obter_tipo_servico():
    response = client.get(
        "/servicos/tipo-servico/1",
        # headers={
        #     "Authorization": f"Bearer {token_funcionario}"
        # }
    )
    assert response.status_code == 200
    assert response.json()["tipo_servico_id"] == 1  


def test_vincular_servico_orcamento(obter_servico, obter_orcamento):
    servico = obter_servico
    orcamento = obter_orcamento
    response = client.patch(
        f"/servicos/{servico.servico_id}/vincular/{orcamento.orcamento_id}",
        # headers={
        #     "Authorization": f"Bearer {token_mecanico}"
        # }
    )
    assert response.status_code == 200
    assert response.json()["orcamento_id"] == orcamento.orcamento_id


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
