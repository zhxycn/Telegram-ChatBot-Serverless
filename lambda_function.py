import json
import os

import httpx

from utils.chat import create_conversation

BOT_TOKEN = os.environ["BOT_TOKEN"]


def send_message(chat_id, text):
    params = {"text": text, "chat_id": chat_id, "parse_mode": "MarkdownV2"}
    httpx.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params=params)


def escape_special_characters(string):
    special_characters = [
        "_",
        "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]
    escaped_string = "".join(
        [f"\\{char}" if char in special_characters else char for char in string]
    )
    return escaped_string


def process_event(event):
    body = json.loads(event["body"])
    message = body.get("message", {})
    if message is not None:
        uid = message.get("from", {}).get("id")
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text")
    else:
        uid = chat_id = text = None
    try:
        if text.startswith("/"):
            command = text.split()[0][1:]
            if command == "user":
                send_message(chat_id, f"*用户信息：*\nUID: `{uid}`")
            if command == "chat":
                try:
                    text = text.split(" ", 1)[1]
                    messages = [{"role": "user", "content": text}]
                    response = escape_special_characters(create_conversation(messages))
                    send_message(chat_id, response)
                except IndexError:
                    send_message(chat_id, "请输入对话内容")
    except AttributeError:
        pass


def lambda_handler(event, context):
    process_event(event)
    return {"statusCode": 200}
