import json
import os
import sys
import time

import openai


def createMessage(side:str, moves : str):
    return f'You are play chess as {side}, select one of the following move:' \
            + f"\n {moves} \n" \
            + "reply with ONLY THE NUMBER"


def prompt(moves: str, side: str) -> str:
    with open(os.path.dirname(__file__) +'/test.config') as file:
        openai.api_key = json.load(file)["openai"]["api_key"]

    messages = [
        {
            "role" : "user",
            "content" : createMessage(side, moves)
        }
    ]

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )

    time.sleep(2)

    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    while not reply.isdigit():
        messages.append(
            {
                "role" : "user",
                "content" : "Just the number please"
            }
        )

        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

        time.sleep(1)

        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

    return reply
