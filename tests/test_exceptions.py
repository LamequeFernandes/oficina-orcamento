"""
Testes unitários de app/core/exceptions.py.
Cobrem todas as classes de exceção e todos os ramos de tratar_erro_dominio.
"""
import pytest
from fastapi import HTTPException
from app.core.exceptions import (
    NaoEncontradoError,
    OrdemServicoNotFoundError,
    VeiculoNotFoundError,
    ClienteNotFoundError,
    FuncionarioNotFoundError,
    SomenteProprietarioDoUsuarioError,
    SomenteProprietarioOuAdminError,
    ApenasAdminPodeAcessarError,
    ApenasMecanicosPodemAcessarError,
    ApenasClientesPodemAcessarError,
    ApenasFuncionariosError,
    ApenasFuncionariosProprietariosError,
    TokenInvalidoError,
    ValidacaoTokenError,
    TamanhoCPFInvalidoError,
    TamanhoCNPJInvalidoError,
    TipoInvalidoClienteError,
    ValorDuplicadoError,
    PadraoPlacaIncorretoError,
    ObjetoPossuiVinculoError,
    ApenasMecanicoResponsavel,
    StatusOSInvalido,
    tratar_erro_dominio,
)


# ---------------------------------------------------------------------------
# Construtores das classes de exceção
# ---------------------------------------------------------------------------

def test_nao_encontrado_error_com_id():
    err = NaoEncontradoError("Orçamento", 42)
    assert "Orçamento" in str(err)
    assert "42" in str(err)


def test_nao_encontrado_error_sem_id():
    err = NaoEncontradoError("Orçamento")
    assert "Orçamento" in str(err)


def test_ordem_servico_not_found_com_id():
    err = OrdemServicoNotFoundError(10)
    assert "10" in str(err)
    assert err.ordem_servico_id == 10


def test_ordem_servico_not_found_sem_id():
    err = OrdemServicoNotFoundError()
    assert err.ordem_servico_id is None


def test_veiculo_not_found_com_id():
    err = VeiculoNotFoundError(5)
    assert "5" in str(err)
    assert err.veiculo_id == 5


def test_veiculo_not_found_sem_id():
    err = VeiculoNotFoundError()
    assert err.veiculo_id is None


def test_cliente_not_found_com_id():
    err = ClienteNotFoundError(3)
    assert "3" in str(err)
    assert err.cliente_id == 3


def test_cliente_not_found_sem_id():
    err = ClienteNotFoundError()
    assert err.cliente_id is None


def test_funcionario_not_found_com_id():
    err = FuncionarioNotFoundError(7)
    assert "7" in str(err)
    assert err.funcionario_id == 7


def test_funcionario_not_found_sem_id():
    err = FuncionarioNotFoundError()
    assert err.funcionario_id is None


def test_somente_proprietario_do_usuario_error():
    err = SomenteProprietarioDoUsuarioError()
    assert "proprietário" in str(err)


def test_somente_proprietario_ou_admin_error():
    err = SomenteProprietarioOuAdminError()
    assert "proprietário" in str(err)


def test_apenas_admin_error():
    err = ApenasAdminPodeAcessarError()
    assert "administradores" in str(err)


def test_apenas_mecanicos_error():
    err = ApenasMecanicosPodemAcessarError()
    assert "mecanicos" in str(err)


def test_apenas_clientes_error():
    err = ApenasClientesPodemAcessarError()
    assert "clientes" in str(err)


def test_apenas_funcionarios_error():
    err = ApenasFuncionariosError()
    assert "funcionários" in str(err)


def test_apenas_funcionarios_proprietarios_error():
    err = ApenasFuncionariosProprietariosError()
    assert "funcionários" in str(err)


def test_token_invalido_error():
    err = TokenInvalidoError()
    assert "Token" in str(err)


def test_validacao_token_error():
    err = ValidacaoTokenError()
    assert "validação" in str(err)


def test_tamanho_cpf_invalido_error():
    err = TamanhoCPFInvalidoError()
    assert "CPF" in str(err)


def test_tamanho_cnpj_invalido_error():
    err = TamanhoCNPJInvalidoError()
    assert "CNPJ" in str(err)


def test_tipo_invalido_cliente_error():
    err = TipoInvalidoClienteError()
    assert "PJ" in str(err) or "PF" in str(err)


def test_valor_duplicado_error():
    err = ValorDuplicadoError("teste@email.com", "email")
    assert "email" in str(err)
    assert err.valor == "teste@email.com"
    assert err.chave == "email"


def test_padrao_placa_incorreto_error():
    err = PadraoPlacaIncorretoError()
    assert "placa" in str(err).lower()


def test_objeto_possui_vinculo_error():
    err = ObjetoPossuiVinculoError("Peça", 1, "Orçamento")
    assert "Peça" in str(err)
    assert "1" in str(err)
    assert err.objeto == "Peça"
    assert err.objeto_id == 1
    assert err.objeto_vinculado == "Orçamento"


def test_apenas_mecanico_responsavel_error():
    err = ApenasMecanicoResponsavel()
    assert "mecânico" in str(err)


def test_status_os_invalido_error():
    err = StatusOSInvalido("ABERTO", "EM_ANDAMENTO")
    assert "ABERTO" in str(err)


# ---------------------------------------------------------------------------
# tratar_erro_dominio — um teste por ramo
# ---------------------------------------------------------------------------

def test_tratar_erro_400_value_error():
    exc = tratar_erro_dominio(ValueError("valor inválido"))
    assert exc.status_code == 400


def test_tratar_erro_400_cpf():
    exc = tratar_erro_dominio(TamanhoCPFInvalidoError())
    assert exc.status_code == 400


def test_tratar_erro_400_cnpj():
    exc = tratar_erro_dominio(TamanhoCNPJInvalidoError())
    assert exc.status_code == 400


def test_tratar_erro_400_tipo_cliente():
    exc = tratar_erro_dominio(TipoInvalidoClienteError())
    assert exc.status_code == 400


def test_tratar_erro_400_placa():
    exc = tratar_erro_dominio(PadraoPlacaIncorretoError())
    assert exc.status_code == 400


def test_tratar_erro_400_veiculo_not_found():
    exc = tratar_erro_dominio(VeiculoNotFoundError(1))
    assert exc.status_code == 400


def test_tratar_erro_400_status_os_invalido():
    exc = tratar_erro_dominio(StatusOSInvalido("A", "B"))
    assert exc.status_code == 400


def test_tratar_erro_401_token_invalido():
    exc = tratar_erro_dominio(TokenInvalidoError())
    assert exc.status_code == 401


def test_tratar_erro_401_validacao_token():
    exc = tratar_erro_dominio(ValidacaoTokenError())
    assert exc.status_code == 401


def test_tratar_erro_403_apenas_admin():
    exc = tratar_erro_dominio(ApenasAdminPodeAcessarError())
    assert exc.status_code == 403


def test_tratar_erro_403_apenas_mecanicos():
    exc = tratar_erro_dominio(ApenasMecanicosPodemAcessarError())
    assert exc.status_code == 403


def test_tratar_erro_403_apenas_clientes():
    exc = tratar_erro_dominio(ApenasClientesPodemAcessarError())
    assert exc.status_code == 403


def test_tratar_erro_403_apenas_funcionarios():
    exc = tratar_erro_dominio(ApenasFuncionariosError())
    assert exc.status_code == 403


def test_tratar_erro_403_apenas_mecanico_responsavel():
    exc = tratar_erro_dominio(ApenasMecanicoResponsavel())
    assert exc.status_code == 403


def test_tratar_erro_403_cliente_not_found():
    exc = tratar_erro_dominio(ClienteNotFoundError(1))
    assert exc.status_code == 403


def test_tratar_erro_403_funcionario_not_found():
    exc = tratar_erro_dominio(FuncionarioNotFoundError(1))
    assert exc.status_code == 403


def test_tratar_erro_403_somente_proprietario():
    exc = tratar_erro_dominio(SomenteProprietarioDoUsuarioError())
    assert exc.status_code == 403


def test_tratar_erro_403_somente_proprietario_ou_admin():
    exc = tratar_erro_dominio(SomenteProprietarioOuAdminError())
    assert exc.status_code == 403


def test_tratar_erro_409_valor_duplicado():
    exc = tratar_erro_dominio(ValorDuplicadoError("abc@email.com", "email"))
    assert exc.status_code == 409
    assert "email" in exc.detail


def test_tratar_erro_500_excecao_desconhecida():
    exc = tratar_erro_dominio(RuntimeError("erro inesperado"))
    assert exc.status_code == 500
