from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from app.core.security import decodificar_token_jwt
# from app.modules.usuario.infrastructure.models import (
#     FuncionarioModel,
#     ClienteModel,
#     UsuarioModel,
# )
from app.core.exceptions import (
    ApenasFuncionariosError,
    ValidacaoTokenError,
    TokenInvalidoError,
    ApenasClientesPodemAcessarError,
    ApenasMecanicosPodemAcessarError,
    ApenasAdminPodeAcessarError,
)

# HTTPBearer apenas extrai o token do header Authorization: Bearer <token>
# A emissão do token é responsabilidade de outro microsserviço (oficina-auth-lambda)
http_bearer = HTTPBearer()


def obter_id_usuario_logado(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> int:
    """Dependência que valida o JWT emitido pelo serviço de autenticação e retorna o ID do usuário."""
    try:
        usuario_id = decodificar_token_jwt(credentials.credentials)
        if usuario_id is None:
            raise TokenInvalidoError
        return usuario_id
    except JWTError:
        raise ValidacaoTokenError

