import os
from uuid import uuid4

# Load environment variables
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Define models and initialize conversation history
models = [
    {"name": "gpt-4", "id": "gpt-4"},
    {"name": "gpt-4-32k", "id": "gpt-4-32k"},
    {"name": "gpt-3.5-turbo", "id": "gpt-3.5-turbo"},
]
conversation_history = []


def create_conversation_item(user_name, text):
    return {"user": user_name, "text": text}


def get_conversation_id():
    # random conversation id ie "7f8ee916-7ccf-46bb-9a2c-3b40913a1558"
    # create random conversation id
    # make it string
    return str(uuid4())


def get_prompt(text_to_send):
    # gets the last items up to 4000 characters in the conversation history
    # iterate over conversation history and add until limit is reached
    # return the prompt
    last_conversation_items = []
    for item in reversed(conversation_history):
        if len(item["text"]) + len(last_conversation_items) > 4000:
            break
        last_conversation_items.append(item)
    last_conversation_items.reverse()
    prompt = ""
    for item in last_conversation_items:
        prompt += f"{item['user']}: {item['text']}\n"
    prompt += "HUMAN: " + text_to_send
    return prompt
