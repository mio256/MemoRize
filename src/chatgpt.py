import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']


def send_messages(messages: list):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=messages,
    )


def send_user_content(content: str):
    return send_messages([
        {
            "role": "user",
            "content": content,
        },
    ])
