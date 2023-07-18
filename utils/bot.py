import os
import httpx

BOT_TOKEN = os.environ["BOT_TOKEN"]
API_URL = "https://api.telegram.org/bot{}/{}"


def send_request(method: str, params: dict) -> None:
    """
    Send a request to the Telegram Bot API.

    :param method: The API method to call.
    :param params: A dictionary containing the request parameters.
    """
    url = API_URL.format(BOT_TOKEN, method)
    httpx.get(url, params=params)


def send_message(chat_id: int, text: str) -> None:
    """
    Send a message to the specified chat ID.

    :param chat_id: The ID of the target chat.
    :param text: The text of the message to send.
    """
    params = {
        "text": text,
        "chat_id": chat_id,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True,
    }
    send_request("sendMessage", params)


def reply_message(chat_id: int, message_id: int, text: str) -> None:
    """
    Reply to a message with the specified message ID.

    :param chat_id: The ID of the target chat.
    :param message_id: The ID of the message to reply to.
    :param text: The text of the reply message to send.
    """
    params = {
        "text": text,
        "chat_id": chat_id,
        "reply_to_message_id": message_id,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True,
    }
    send_request("sendMessage", params)


def edit_message(chat_id: int, message_id: int, text: str) -> None:
    """
    Edit a message with the specified message ID.

    :param chat_id: The ID of the target chat.
    :param message_id: The ID of the message to edit.
    :param text: The edited text of the message.
    """
    params = {
        "text": text,
        "chat_id": chat_id,
        "message_id": message_id,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True,
    }
    send_request("editMessageText", params)


def delete_message(chat_id: int, message_id: int) -> None:
    """
    Delete a message with the specified message ID.

    :param chat_id: The ID of the target chat.
    :param message_id: The ID of the message to delete.
    """
    params = {
        "chat_id": chat_id,
        "message_id": message_id,
    }
    send_request("deleteMessage", params)


def send_chat_action(chat_id: int, action: str) -> None:
    """
    Send a chat action to the specified chat ID.

    :param chat_id: The ID of the target chat.
    :param action: The chat action to send.
    """
    params = {
        "chat_id": chat_id,
        "action": action,
    }
    send_request("sendChatAction", params)
