import os

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


def create_conversation(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
    )
    return response["choices"][0]["message"]["content"]
