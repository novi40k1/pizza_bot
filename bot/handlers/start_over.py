import json

from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus


class StartOverHandler(Handler):
    def can_handle(self, update: dict, state: str, data: dict,storage : Storage, messenger: Messenger) -> bool:
        if "callback_query" not in update:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data == "start_over"

    def handle(self, update: dict, state: str, data: dict,storage : Storage, messenger: Messenger) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]

        storage.clear_user_state_and_order(telegram_id)
        storage.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

        messenger.answerCallbackQuery(update["callback_query"]["id"])
        messenger.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )
        messenger.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="🔄 Starting over... Please choose pizza name",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Margherita", "callback_data": "pizza_margherita"},
                            {"text": "Pepperoni", "callback_data": "pizza_pepperoni"},
                        ],
                        [
                            {
                                "text": "Quattro Stagioni",
                                "callback_data": "pizza_quattro_stagioni",
                            },
                            {
                                "text": "Capricciosa",
                                "callback_data": "pizza_capricciosa",
                            },
                        ],
                        [
                            {"text": "Diavola", "callback_data": "pizza_diavola"},
                            {"text": "Prosciutto", "callback_data": "pizza_prosciutto"},
                        ],
                    ],
                }
            ),
        )
        return HandlerStatus.STOP
