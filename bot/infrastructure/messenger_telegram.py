import json
import os
import urllib.request
from dotenv import load_dotenv
from bot.domain.messenger import Messenger

load_dotenv()


class MessengerTelegram(Messenger):
    def make_request(self, method: str, **param) -> dict:
        json_data = json.dumps(param).encode("utf-8")
        request = urllib.request.Request(
            method="POST",
            url=f"{os.getenv('TELEGRAM_BASE_URI')}/{method}",
            data=json_data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            response_json = json.loads(response_body)
            assert response_json["ok"] is True
            return response_json["result"]

    def getUpdates(self, **params) -> dict:
        return self.make_request("getUpdates", **params)

    def sendMessage(self, chat_id: int, text: str, **params) -> dict:
        return self.make_request("sendMessage", chat_id=chat_id, text=text, **params)

    def getMe(self) -> dict:
        return self.make_request("getMe")

    def deleteMessage(self, chat_id: int, message_id: int) -> dict:
        return self.make_request(
            "deleteMessage", chat_id=chat_id, message_id=message_id
        )

    def answerCallbackQuery(self, callback_query_id: str, **params) -> dict:
        return self.make_request(
            "answerCallbackQuery", callback_query_id=callback_query_id, **params
        )
