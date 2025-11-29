from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    async def ensure_user_exists(self, telegram_id: int) -> None: ...

    @abstractmethod
    async def clear_user_state_and_order(self, telegram_id: int) -> None: ...

    @abstractmethod
    async def update_user_state(self, telegram_id: int, state: str) -> None: ...

    @abstractmethod
    async def persist_update(self, update: dict) -> None: ...

    @abstractmethod
    async def update_user_order_json(
        self, telegram_id: int, order_json: dict
    ) -> None: ...

    @abstractmethod
    async def recreate_database(self) -> None: ...

    @abstractmethod
    async def get_user(self, telegram_id: int) -> dict: ...
