import aiohttp

from settings import settings


class AuthClient:
    """
    Клиент для обращения к Auth-сервису.
    Использует aiohttp для асинхронных запросов.
    """

    def __init__(self):
        """
        Инициализация клиента.
        Args:
            base_url (str): Базовый URL сервиса авторизации.
        """
        self.base_url = settings.AUTH_SERVICE_URL

    async def get_public_key(self) -> str:
        """
        Получает публичный ключ от Auth-сервиса.
        Returns:
            str: Публичный ключ в формате PEM.
        Raises:
            RuntimeError: Если запрос завершился ошибкой.
        """
        url = f"{self.base_url}{settings.PUBLIC_KEY_PATH}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"Ошибка при получении public key: {resp.status}")
                data = await resp.json()
                return data["public_key"]
