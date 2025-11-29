import json
import asyncio

from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus


class PizzaDrinksHandler(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_DRINKS":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    async def handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        drink_mapping = {
            "drink_coca_cola": "Coca-Cola",
            "drink_pepsi": "Pepsi",
            "drink_orange_juice": "Orange Juice",
            "drink_apple_juice": "Apple Juice",
            "drink_water": "Water",
            "drink_iced_tea": "Iced Tea",
            "drink_none": "No drinks",
        }

        drink = drink_mapping.get(callback_data)
        data["drink"] = drink
        await asyncio.gather(
            storage.update_user_order_json(telegram_id, data),
            storage.update_user_state(telegram_id, "WAIT_FOR_ORDER_APPROVE"),
            messenger.answerCallbackQuery(update["callback_query"]["id"]),
            messenger.deleteMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                message_id=update["callback_query"]["message"]["message_id"],
            ),
        )

        order_summary = f"""
✅ Your order:
🍕 Pizza: {data['pizza_name']}
📏 Size: {data['pizza_size']}
🥤 Drink: {drink}

Please confirm your order:
        """

        await messenger.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text=order_summary,
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "✅ Confirm", "callback_data": "order_confirm"},
                            {"text": "❌ Cancel", "callback_data": "order_cancel"},
                        ],
                        [{"text": "🔄 Start Over", "callback_data": "start_over"}],
                    ]
                }
            ),
        )
        return HandlerStatus.STOP
