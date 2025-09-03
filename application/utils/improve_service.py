class ImproveClient:
    """
    Клиент для обращения к сервису,
    улучшающего содержание текста (AL может как вариант,
    быть в другом микросервисе)
    """
    def improve_resume(self, text: str) -> str:
        """Функция для улучшения содержания резюме

        Args:
            text (str): Содержание резюме

        Returns:
            str: Улучшенное содержание резюме
        """
        return text + " [Improved]"