import json

import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus


class StartOverHandler(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data == "start_over"

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]

        bot.database_client.clear_user_state_and_order(telegram_id)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"])
        bot.telegram_client.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )
        bot.telegram_client.sendMessage(
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
