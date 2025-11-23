from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus


class OrderApprovalHandler(Handler):
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

        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data in ["order_confirm", "order_cancel"]

    def handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        messenger.answerCallbackQuery(update["callback_query"]["id"])
        messenger.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        if callback_data == "order_confirm":
            storage.update_user_state(telegram_id, "ORDER_FINISHED")

            order_summary = f"""
🎉 Order confirmed!
Thank you for your order!

📋 Order details:
🍕 Pizza: {data['pizza_name']}
📏 Size: {data['pizza_size']}
🥤 Drink: {data.get('drink', 'No drinks')}

Your order will be ready in 30 minutes!
            """

            messenger.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text=order_summary,
            )
        else:
            storage.clear_user_state_and_order(telegram_id)
            messenger.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text="❌ Order canceled. To start over, send /start",
            )

        return HandlerStatus.STOP
