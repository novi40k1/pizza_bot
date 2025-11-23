from bot.dispatcher import Dispatcher
from bot.handlers.pizza_size import PizzaSizeHandler

from tests.mock import Mock


def test_pizza_size_handler():
    test_update = {
        "update_id": 123456789,
        "callback_query": {
            "id": "test_callback_id",
            "from": {
                "id": 12345,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser",
            },
            "message": {
                "message_id": 100,
                "chat": {
                    "id": 12345,
                    "first_name": "Test",
                    "username": "testuser",
                    "type": "private",
                },
            },
            "data": "size_medium",
        },
    }

    # Track method calls
    update_user_order_json_called = False
    update_user_state_called = False
    answer_callback_query_called = False
    delete_message_called = False
    send_message_called = False

    def update_user_order_json(telegram_id: int, order_data: dict) -> None:
        assert telegram_id == 12345
        assert order_data == {
            "pizza_name": "Margherita",
            "pizza_size": "Medium (30cm)"
        }
        nonlocal update_user_order_json_called
        update_user_order_json_called = True

    def update_user_state(telegram_id: int, state: str) -> None:
        assert telegram_id == 12345
        assert state == "WAIT_FOR_DRINKS"
        nonlocal update_user_state_called
        update_user_state_called = True

    def answerCallbackQuery(callback_query_id: str) -> dict:
        assert callback_query_id == "test_callback_id"
        nonlocal answer_callback_query_called
        answer_callback_query_called = True
        return {"ok": True}

    def deleteMessage(chat_id: int, message_id: int) -> dict:
        assert chat_id == 12345
        assert message_id == 100
        nonlocal delete_message_called
        delete_message_called = True
        return {"ok": True}

    def sendMessage(chat_id: int, text: str, **kwargs) -> dict:
        assert chat_id == 12345
        assert text == "Please choose some drinks"
        assert "reply_markup" in kwargs
        nonlocal send_message_called
        send_message_called = True
        return {"ok": True}

    def get_user(telegram_id: int) -> dict:
        assert telegram_id == 12345
        return {
            "id": 1,
            "telegram_id": 12345,
            "state": "WAIT_FOR_PIZZA_SIZE",
            "order_json": '{"pizza_name": "Margherita"}'
        }

    mock_storage = Mock({
        "update_user_order_json": update_user_order_json,
        "update_user_state": update_user_state,
        "get_user": get_user,
    })

    mock_messenger = Mock({
        "answerCallbackQuery": answerCallbackQuery,
        "deleteMessage": deleteMessage,
        "sendMessage": sendMessage,
    })

    dispatcher = Dispatcher(mock_storage, mock_messenger)
    dispatcher.add_handlers(PizzaSizeHandler())
    dispatcher.dispatch(test_update)

    # Verify all expected methods were called
    assert update_user_order_json_called
    assert update_user_state_called
    assert answer_callback_query_called
    assert delete_message_called
    assert send_message_called


def test_pizza_size_handler_wrong_state():
    """Test that handler doesn't process when state is incorrect"""
    test_update = {
        "update_id": 123456789,
        "callback_query": {
            "id": "test_callback_id",
            "from": {"id": 12345},
            "message": {"message_id": 100, "chat": {"id": 12345}},
            "data": "size_medium",
        },
    }

    def get_user(telegram_id: int) -> dict:
        return {
            "id": 1,
            "telegram_id": 12345,
            "state": "WRONG_STATE",  # Wrong state for this handler
            "order_json": "{}"
        }

    mock_storage = Mock({
        "get_user": get_user,
    })
    mock_messenger = Mock({})

    handler = PizzaSizeHandler()
    can_handle = handler.can_handle(
        test_update,
        "WRONG_STATE",
        {"pizza_name": "Margherita"},
        mock_storage,
        mock_messenger
    )

    assert not can_handle


def test_pizza_size_handler_wrong_callback_data():
    """Test that handler doesn't process when callback data is incorrect"""
    test_update = {
        "update_id": 123456789,
        "callback_query": {
            "id": "test_callback_id",
            "from": {"id": 12345},
            "message": {"message_id": 100, "chat": {"id": 12345}},
            "data": "wrong_callback_data",  # Wrong callback data
        },
    }

    def get_user(telegram_id: int) -> dict:
        return {
            "id": 1,
            "telegram_id": 12345,
            "state": "WAIT_FOR_PIZZA_SIZE",
            "order_json": "{}"
        }

    mock_storage = Mock({
        "get_user": get_user,
    })
    mock_messenger = Mock({})

    handler = PizzaSizeHandler()
    can_handle = handler.can_handle(
        test_update,
        "WAIT_FOR_PIZZA_SIZE",
        {"pizza_name": "Margherita"},
        mock_storage,
        mock_messenger
    )

    assert not can_handle