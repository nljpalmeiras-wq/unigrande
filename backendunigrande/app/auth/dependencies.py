from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.config.settings import ALGORITHM, OAUTH2_SCHEME, SECRET_KEY


def verify_token(token: str = Depends(OAUTH2_SCHEME)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Verificar se o token contém o 'sub' (email ou id)
        if "email" not in payload:  # Aqui você pode verificar o campo que preferir
            raise credentials_exception

        # Retorna o payload para ser usado nos endpoints
        return payload

    except JWTError:
        raise credentials_exception  # Se ocorrer erro na decodificação
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar o token: {str(e)}",
        )
