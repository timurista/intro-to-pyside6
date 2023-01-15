import asyncio
import json
import os

conversation_history = []

def create_conversation_item(user_name, text):
    return {
        "user": user_name,
        "text": text
    }

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
    prompt += "HUMAN: "+prompt_engineering(text_to_send)
    return prompt


def prompt_engineering(prompt_test):
    truthfullness_statement = "Answer the question as truthfully as possible, and if you're very unsure of the answer, say \"Sorry, I don't know\""
    return prompt_test
    # return f"""{truthfullness_statement}. {prompt_test}"""
