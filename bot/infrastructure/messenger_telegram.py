import os
import logging
import time
import aiohttp
from dotenv import load_dotenv
from bot.domain.messenger import Messenger

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s.%(msecs)03d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class MessengerTelegram(Messenger):
    def __init__(self) -> None:
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def make_request(self, method: str, **param) -> dict:
        url = f"{os.getenv('TELEGRAM_BASE_URI')}/{method}"
        start_time = time.time()
        logger.info(f"[HTTP] → POST {method}")

        try:
            session = await self._get_session()
            async with session.post(
                url,
                json=param,
                headers={"Content-Type": "application/json"},
            ) as response:
                response_json = await response.json()
                assert response_json["ok"] == True  # noqa: E712

                duration_ms = (time.time() - start_time) * 1000
                logger.info(f"[HTTP] ← POST {method} - {duration_ms:.2f}ms")

                return response_json["result"]
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(f"[HTTP] ✗ POST {method} - {duration_ms:.2f}ms - Error: {e}")
            raise

    async def close(self) -> None:
        """Закрыть HTTP сессию."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def getUpdates(self, **params) -> dict:
        return await self.make_request("getUpdates", **params)

    async def sendMessage(self, chat_id: int, text: str, **params) -> dict:
        return await self.make_request(
            "sendMessage", chat_id=chat_id, text=text, **params
        )

    async def deleteMessage(self, chat_id: int, message_id: int) -> dict:
        return await self.make_request(
            "deleteMessage", chat_id=chat_id, message_id=message_id
        )

    async def answerCallbackQuery(self, callback_query_id: str, **params) -> dict:
        return await self.make_request(
            "answerCallbackQuery", callback_query_id=callback_query_id, **params
        )
