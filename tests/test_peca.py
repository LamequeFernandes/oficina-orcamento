from fastapi.testclient import TestClient
from app.main import app
from app.modules.orcamento.domain.entities import StatusOrcamento


client = TestClient(app, raise_server_exceptions=False)


def test_adiciona_peca():
    response = client.post(
        f"/pecas",
        json={
            "tipo_peca_id": 1,
            "valor_peca": 100.0,
            "marca": "Marca Exemplo",
        },
        # headers={
        #     "Authorization": f"Bearer {token_mecanico}"
        # }
    )
    assert response.status_code == 201


def test_obter_peca(obter_peca):
    peca = obter_peca
    response = client.get(
        f"/pecas/{peca.peca_id}",
        # headers={
        #     "Authorization": f"Bearer {token_mecanico}"
        # }
    )
    assert response.status_code == 200
    assert response.json() == peca.dict()


def test_listar_tipo_pecas():
    response = client.get(
        f"/pecas/tipo-peca",
        # headers={
        #     "Authorization": f"Bearer {token_mecanico}"
        # }
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_vincular_peca_orcamento(obter_peca, obter_orcamento):
    orcamento = obter_orcamento
    peca = obter_peca
    response = client.patch(
        f"/pecas/{peca.peca_id}/vincular/{orcamento.orcamento_id}",
        # headers={
        #     "Authorization": f"Bearer {token_mecanico}"
        # }
    )
    assert response.status_code == 200
    assert response.json()["orcamento_id"] == orcamento.orcamento_id




