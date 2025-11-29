from abc import ABC, abstractmethod


class Messenger(ABC):
    @abstractmethod
    async def sendMessage(self, chat_id: int, text: str, **kwargs) -> dict: ...

    @abstractmethod
    async def getUpdates(self, **kwargs) -> dict: ...

    @abstractmethod
    async def answerCallbackQuery(self, callback_query_id: str, **kwargs) -> dict: ...

    @abstractmethod
    async def deleteMessage(self, chat_id: int, message_id: int) -> dict: ...
