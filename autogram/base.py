import re
import json
import requests
import threading
from abc import ABC
from typing import Any
from . import ChatAction
from loguru import logger
from requests.models import Response
from autogram.config import save_config


# --
class Bot(ABC):
    endpoint = "https://api.telegram.org/"
    register = {"lock": threading.Lock(), "handlers": dict()}

    # --
    @classmethod
    def add(cls, name: str):
        def wrapper(fn):
            logger.debug(fn.__name__)
            with cls.register["lock"]:
                cls.register["handlers"] |= {name: fn}
            return fn

        return wrapper

    # --
    def __init__(self, initializer: threading.Event, config: dict) -> None:
        self.config = config
        self.requests = requests.session()
        if proxies := config.get("proxies"):
            self.requests.proxies = proxies
        assert self.config.get("telegram-token"), "Missing bot token!"
        # init complete
        initializer.set()
        logger.debug("initialization complete!")

    def data(self, key: str, val: Any | None = None) -> Any:
        """Persistent data storage"""
        self.config["data"] = self.config.get("data") or dict()
        if val:
            self.config["data"].update({key: val})
            return save_config(self.config)
        return self.config["data"].get(key)

    def settings(self, key: str, val: Any | None = None) -> Any:
        """Get or set value of key in config"""
        if val:
            self.config.update({key: val})
            return save_config(self.config)
        return self.config.get(key)

    def setWebhook(self, hook_addr: str, **kwargs):
        """kwargs update setWebhook parameters with higher precendence. Existing(url, allowed_updates)"""
        if not re.search("^(https?):\\/\\/[^\\s/$.?#].[^\\s]*$", hook_addr):
            raise RuntimeError("Invalid webhook url. format <https://...>")
        # --
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/setWebhook'
        with self.register["lock"]:
            params = {
                "url": hook_addr,
                "allowed_updates": json.dumps(list(self.register["handlers"].keys())),
            } | kwargs
        return self.requests.get(url, params=params)

    def poll(self, offset=0, limit=10, timeout=7):
        """Poll updates for registered handlers only. Use getUpdates for unfiltered."""
        with self.register["lock"]:
            data = {
                "timeout": timeout,
                "params": {
                    "allowed_updates": json.dumps(
                        list(self.register["handlers"].keys())
                    ),
                    "timeout": timeout // 2,
                    "offset": offset,
                    "limit": limit,
                },
            }
        return self.getUpdates(**data)

    def getMe(self) -> Response:
        """Fetch `bot` information"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/getMe'
        return self.requests.get(url)

    def getUpdates(self, **kwargs) -> Response:
        """Poll for updates"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/getUpdates'
        return self.requests.get(url, **kwargs)

    def downloadFile(self, file_path: str) -> Response:
        """Downloads a file with file_path got from getFile(...)"""
        url = f'{self.endpoint}file/bot{self.settings("telegram-token")}/{file_path}'
        return self.requests.get(url)

    def getFile(self, file_id: str) -> Response:
        """Gets details of file with file_id"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/getFile'
        return self.requests.get(url, params={"file_id": file_id})

    def getChat(self, chat_id: int) -> Response:
        """Gets information on chat_id"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/getChat'
        return self.requests.get(url, params={"chat_id": chat_id})

    def getWebhookInfo(self) -> Response:
        """Gets information on currently set webhook"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/getWebhookInfo'
        return self.requests.get(url)

    def sendChatAction(self, chat_id: int, action: str) -> Response:
        """Sends `action` to chat_id"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/sendChatAction'
        params = {"chat_id": chat_id, "action": action}
        return self.requests.get(url, params=params)

    def sendMessage(self, chat_id: int | str, text: str, **kwargs) -> Response:
        """Sends `text` to `chat_id`"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/sendMessage'
        params = {
            "chat_id": chat_id,
            "text": text,
        } | kwargs
        return self.requests.get(url, params=params)

    def deleteMessage(self, chat_id: int, msg_id: int) -> Response:
        """Deletes message sent <24hrs ago"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/deleteMessage'
        params = {"chat_id": chat_id, "message_id": msg_id}
        return self.requests.get(url, params=params)

    def deleteWebhook(self, drop_pending=False) -> Response:
        """Deletes webhook value"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/deleteWebhook'
        return self.requests.get(url, params={"drop_pending_updates": drop_pending})

    def editMessageText(
        self, chat_id: int, msg_id: int, text: str, **kwargs
    ) -> Response:
        """Edit message sent <24hrs ago"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/editMessageText'
        params = {"text": text, "chat_id": chat_id, "message_id": msg_id} | kwargs
        return self.requests.get(url, params=params)

    def editMessageCaption(
        self, chat_id: int, msg_id: int, capt: str, **kwargs
    ) -> Response:  # noqa: E501
        """Edit message caption"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/editMessageCaption'
        params = {"chat_id": chat_id, "message_id": msg_id, "caption": capt} | kwargs
        return self.requests.get(url, params=params)

    def editMessageReplyMarkup(
        self, chat_id: int, msg_id: int, markup: str, **kwargs
    ) -> Response:  # noqa: E501
        """Edit reply markup"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/editMessageReplyMarkup'
        params = {
            "chat_id": chat_id,
            "message_id": msg_id,
            "reply_markup": markup,
        } | kwargs
        return self.requests.get(url, params=params)

    def forwardMessage(self, chat_id: int, from_chat_id: int, msg_id: int) -> Response:
        """Forward message with message_id from from_chat_id to chat_id"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/forwardMessage'
        params = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": msg_id,
        }
        return self.requests.get(url, params=params)

    def answerCallbackQuery(
        self, query_id, text: str | None = None, **kwargs
    ) -> Response:  # noqa: E501
        """Answers callback queries with text: str of len(text) < 200"""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/answerCallbackQuery'
        text = text or "Updated!"
        params = {"callback_query_id": query_id, "text": text[:200]} | kwargs
        return self.requests.get(url, params=params)

    def sendPhoto(self, chat_id: int, photo: bytes | str, **kwargs) -> Response:  # noqa: E501
        """Sends a photo to a telegram user"""
        """kwargs: caption, etc."""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/sendPhoto'
        filename = kwargs.pop("filename") if "filename" in kwargs else None
        params = {"chat_id": chat_id} | kwargs
        self.sendChatAction(chat_id, ChatAction.photo)
        if isinstance(photo, str):
            return self.requests.get(url, params=params | {"photo": photo})
        if filename:
            return self.requests.get(
                url, params=params, files={"photo": (filename, photo)}
            )
        return self.requests.get(url, params=params, files={"photo": photo})

    def sendAudio(self, chat_id: int, audio: bytes | str, **kwargs) -> Response:  # noqa: E501
        """Sends an audio to a telegram user"""
        """kwargs: caption, etc."""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/sendAudio'
        filename = kwargs.pop("filename") if "filename" in kwargs else None
        params = {"chat_id": chat_id} | kwargs
        self.sendChatAction(chat_id, ChatAction.audio)
        if isinstance(audio, str):
            return self.requests.get(url, params=params | {"audio": audio})
        if filename:
            return self.requests.get(
                url, params=params, files={"audio": (filename, audio)}
            )
        return self.requests.get(url, params=params, files={"audio": audio})

    def sendDocument(self, chat_id: int, document: bytes | str, **kwargs) -> Response:  # noqa: E501
        """Sends a document to a telegram user"""
        """kwargs: caption, etc."""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/sendDocument'
        filename = kwargs.pop("filename") if "filename" in kwargs else None
        params = {"chat_id": chat_id} | kwargs
        self.sendChatAction(chat_id, ChatAction.document)
        if isinstance(document, str):
            return self.requests.get(url, params=params | {"document": document})
        if filename:
            return self.requests.get(
                url, params=params, files={"document": (filename, document)}
            )
        return self.requests.get(url, params=params, files={"document": document})

    def sendVideo(self, chat_id: int, video: bytes | str, **kwargs) -> Response:  # noqa: E501
        """Sends a video to a telegram user"""
        """kwargs: caption, etc."""
        url = f'{self.endpoint}bot{self.settings("telegram-token")}/sendVideo'
        filename = kwargs.pop("filename") if "filename" in kwargs else None
        params = {"chat_id": chat_id} | kwargs
        self.sendChatAction(chat_id, ChatAction.video)
        if isinstance(video, str):
            return self.requests.get(url, params=params | {"video": video})
        if filename:
            return self.requests.get(
                url, params=params, files={"video": (filename, video)}
            )
        return self.requests.get(url, params=params, files={"video": video})

    def forceReply(self, **kwargs) -> str:
        """Returns forceReply value as string"""
        markup = {
            "force_reply": True,
        } | kwargs
        return json.dumps(markup)

    def getKeyboardMarkup(self, keys: list, **kwargs) -> str:
        """Returns keyboard markup as string"""
        markup = {"keyboard": [row for row in keys]} | kwargs
        return json.dumps(markup)

    def getInlineKeyboardMarkup(self, keys: list, **kwargs) -> str:
        markup = {"inline_keyboard": keys} | kwargs
        return json.dumps(markup)

    def removeKeyboard(self, **kwargs) -> str:
        markup = {
            "remove_keyboard": True,
        } | kwargs
        return json.dumps(markup)
