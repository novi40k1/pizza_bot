
import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus


class OrderApprovalHandler(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data in ["order_confirm", "order_cancel"]

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"])
        bot.telegram_client.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        if callback_data == "order_confirm":
            bot.database_client.update_user_state(telegram_id, "ORDER_FINISHED")

            order_summary = f"""
🎉 Order confirmed!
Thank you for your order!

📋 Order details:
🍕 Pizza: {data['pizza_name']}
📏 Size: {data['pizza_size']}
🥤 Drink: {data.get('drink', 'No drinks')}

Your order will be ready in 30 minutes!
            """

            bot.telegram_client.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text=order_summary,
            )
        else:
            bot.database_client.clear_user_state_and_order(telegram_id)
            bot.telegram_client.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text="❌ Order canceled. To start over, send /start",
            )

        return HandlerStatus.STOP
