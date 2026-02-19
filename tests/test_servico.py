from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app, raise_server_exceptions=False)


def test_lista_tipo_servico():
    response = client.get("/servicos/tipo-servico")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_obter_tipo_servico():
    response = client.get("/servicos/tipo-servico/1")
    assert response.status_code == 200
    assert response.json()["tipo_servico_id"] == 1


def test_obter_tipo_servico_inexistente():
    response = client.get("/servicos/tipo-servico/999999")
    assert response.status_code in (404, 500)


def test_criar_servico():
    response = client.post(
        "/servicos",
        json={"tipo_servico_id": 1, "valor_servico": 250.0, "orcamento_id": None},
    )
    assert response.status_code == 201
    assert response.json()["valor_servico"] == 250.0


def test_obter_servico(obter_servico):
    servico = obter_servico
    response = client.get(f"/servicos/{servico.servico_id}")
    assert response.status_code == 200
    assert response.json()["servico_id"] == servico.servico_id


def test_obter_servico_inexistente():
    response = client.get("/servicos/999999")
    assert response.status_code in (404, 500)


def test_alterar_servico(obter_servico):
    servico = obter_servico
    response = client.put(
        f"/servicos/{servico.servico_id}",
        json={"tipo_servico_id": 1, "valor_servico": 300.0, "orcamento_id": None},
    )
    assert response.status_code == 200
    assert response.json()["valor_servico"] == 300.0


def test_vincular_servico_orcamento(obter_servico, obter_orcamento):
    servico = obter_servico
    orcamento = obter_orcamento
    response = client.patch(
        f"/servicos/{servico.servico_id}/vincular/{orcamento.orcamento_id}"
    )
    assert response.status_code == 200
    assert response.json()["orcamento_id"] == orcamento.orcamento_id


def test_desvincular_servico(obter_servico, obter_orcamento):
    servico = obter_servico
    orcamento = obter_orcamento
    # Vincula primeiro
    client.patch(f"/servicos/{servico.servico_id}/vincular/{orcamento.orcamento_id}")
    # Desvincula
    response = client.patch(f"/servicos/{servico.servico_id}/desvincular")
    assert response.status_code == 200
    assert response.json()["orcamento_id"] is None


def test_remover_servico():
    create = client.post(
        "/servicos",
        json={"tipo_servico_id": 2, "valor_servico": 50.0, "orcamento_id": None},
    )
    assert create.status_code == 201
    servico_id = create.json()["servico_id"]

    response = client.delete(f"/servicos/{servico_id}")
    assert response.status_code == 204
