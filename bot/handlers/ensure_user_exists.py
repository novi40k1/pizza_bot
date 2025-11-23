from bot.domain.messenger import Messenger
from bot.handlers.handler import Handler, HandlerStatus
from bot.domain.storage import Storage

class EnsureUserExists(Handler):
    def can_handle(self, update: dict, state: str, data: dict,storage : Storage, messenger: Messenger) -> bool:
        # This handler should run for any update that has a user ID
        return "message" in update and "from" in update["message"]

    def handle(self, update: dict, state: str, data: dict,storage : Storage, messenger: Messenger) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]

        # Ensure user exists (check and create if needed in single transaction)
        storage.ensure_user_exists(telegram_id)

        # Continue processing with other handlers
        return HandlerStatus.CONTINUE
