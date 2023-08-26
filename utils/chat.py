import os

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


def create_conversation(messages: list):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
    )
    content = response["choices"][0]["message"]["content"]
    model = response["model"]
    tokens = [
        response["usage"]["total_tokens"],
        response["usage"]["prompt_tokens"],
        response["usage"]["completion_tokens"],
    ]
    return content, model, tokens
