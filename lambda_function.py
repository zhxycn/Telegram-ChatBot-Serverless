import json

import utils.bot as bot
from utils.chat import create_conversation


def escape_special_characters(string: str) -> str:
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
        message_id = message.get("message_id")
        text = message.get("text")
    else:
        uid = chat_id = message_id = text = None
    try:
        if text.startswith("/"):
            command = text.split()[0][1:]
            if command == "user":
                bot.send_message(chat_id, f"*用户信息：*\nUID: `{uid}`")
            if command == "chat":
                try:
                    text = text.split(" ", 1)[1]
                    messages = [{"role": "user", "content": text}]
                    bot.send_chat_action(chat_id, "typing")
                    conversation = create_conversation(messages)
                    content = escape_special_characters(conversation[0])
                    model = conversation[1]
                    tokens = conversation[2]
                    response = (
                        f"{content}\n\n"
                        f"\-\-\-\-\-\-\-\-\-\- *Information* \-\-\-\-\-\-\-\-\-\-\n"
                        f"Model: `{model}`\n"
                        f"Tokens: `{tokens[0]}({tokens[1]}\+{tokens[2]})`"
                    )
                    bot.reply_message(chat_id, message_id, response)
                except IndexError:
                    bot.reply_message(chat_id, message_id, "请输入对话内容")
    except AttributeError:
        pass


def lambda_handler(event, context):
    process_event(event)
    return {"statusCode": 200}
