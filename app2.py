import asyncio
import functools
import os
import sys
from asyncio import CancelledError
from uuid import uuid4

import openai
import qasync
from dotenv import load_dotenv
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QProgressBar,
                               QPushButton, QSplashScreen, QTextEdit,
                               QVBoxLayout, QWidget)
from qt_material import apply_stylesheet

load_dotenv()

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

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChatGPT Desktop Client")

        # Create the input field
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Enter your prompt here")

        # Create the generate button
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_text)

        # Create a stop button
        self.stop_button = QPushButton("Stop")
        self.
