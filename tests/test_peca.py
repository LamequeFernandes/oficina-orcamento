from fastapi.testclient import TestClient
from app.main import app
from app.modules.orcamento.domain.entities import StatusOrcamento


client = TestClient(app, raise_server_exceptions=False)


def test_adiciona_peca():
    response = client.post(
        "/pecas",
        json={
            "tipo_peca_id": 1,
            "valor_peca": 100.0,
            "marca": "Marca Exemplo",
        },
    )
    assert response.status_code == 201


def test_obter_peca(obter_peca):
    peca = obter_peca
    response = client.get(f"/pecas/{peca.peca_id}")
    assert response.status_code == 200
    assert response.json() == peca.dict()


def test_obter_peca_inexistente():
    response = client.get("/pecas/999999")
    assert response.status_code in (404, 500)


def test_listar_tipo_pecas():
    response = client.get("/pecas/tipo-peca")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_listar_pecas():
    response = client.get("/pecas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_alterar_peca(obter_peca):
    peca = obter_peca
    response = client.put(
        f"/pecas/{peca.peca_id}",
        json={
            "tipo_peca_id": 1,
            "valor_peca": 200.0,
            "marca": "Marca Atualizada",
        },
    )
    assert response.status_code == 200
    assert response.json()["valor_peca"] == 200.0


def test_vincular_peca_orcamento(obter_peca, obter_orcamento):
    orcamento = obter_orcamento
    peca = obter_peca
    response = client.patch(
        f"/pecas/{peca.peca_id}/vincular/{orcamento.orcamento_id}"
    )
    assert response.status_code == 200
    assert response.json()["orcamento_id"] == orcamento.orcamento_id


def test_desvincular_peca(obter_peca, obter_orcamento):
    orcamento = obter_orcamento
    peca = obter_peca
    # Vincula primeiro
    client.patch(f"/pecas/{peca.peca_id}/vincular/{orcamento.orcamento_id}")
    # Desvincula
    response = client.patch(f"/pecas/{peca.peca_id}/desvincular")
    assert response.status_code == 200
    assert response.json()["orcamento_id"] is None
