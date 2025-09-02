from typing import Optional, Dict, Any

from jose import JWTError, jwt
from settings import settings


class JWTTokenService:
    """
    Сервис для декодирования JWT токенов.
    """

    @staticmethod
    def decode_jwt_token(token: str, public_key: str) -> Optional[Dict[str, Any]]:
        """
        Декодирует и проверяет JWT токен.
        Args:
            token (str): JWT токен.
        Returns:
            Optional[Dict[str, Any]]:
                - словарь с расшифрованными данными, если токен валиден;
                - None, если токен невалидный или не соответствует схеме.
        """
        try:
            decode_token = jwt.decode(
                token,
                public_key,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except (JWTError, AttributeError):
            return None

        if set(decode_token.keys()) != {"id", "exp", "type"}:
            return None

        return decode_token
