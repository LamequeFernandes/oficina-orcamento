import pytest
from app.core.database import SessionLocal
from app.modules.orcamento.application.dto import OrcamentoOutputDTO
from app.modules.orcamento.domain.entities import StatusOrcamento
# from app.modules.ordem_servico.application.dto import OrdemServicoOutputDTO
from app.modules.peca.application.dto import PecaInputDTO, PecaOutDTO
from app.modules.servico.application.dto import ServicoOutDTO
# from app.modules.usuario.application.dto import ClienteOutputDTO, FuncionarioOutputDTO
# from app.modules.usuario.infrastructure.models import UsuarioModel, ClienteModel, FuncionarioModel
from fastapi.testclient import TestClient
from app.main import app
# from app.modules.veiculo.application.dto import VeiculoInputDTO


from app.core.database import Base, engine

from app.core.__all_models import *  # noqa: F401
Base.metadata.create_all(bind=engine)

db = SessionLocal()
db.add_all(servicos)
db.add_all(pecas)
db.commit()


client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def obter_orcamento():
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
    yield OrcamentoOutputDTO(**response.json())


@pytest.fixture
def obter_peca():
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
    yield PecaOutDTO(**response.json())


@pytest.fixture
def obter_servico(obter_orcamento):
    orcamento = obter_orcamento
    response = client.post(
        f"/servicos",
        json={
            "tipo_servico_id": 1,
            "valor_servico": 150,
            "orcamento_id": orcamento.orcamento_id
        },
        # headers={
        #     "Authorization": f"Bearer {token_mecanico}"
        # }
    )
    assert response.status_code == 201
    yield ServicoOutDTO(**response.json())
