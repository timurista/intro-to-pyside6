import asyncio
import functools
import json
import os
import sys
from asyncio import CancelledError
from uuid import uuid4

import openai
import PySide6.QtGui as QtGui
import qasync
from dotenv import load_dotenv
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
                               QLineEdit, QProgressBar, QPushButton,
                               QSizePolicy, QTextEdit, QVBoxLayout, QWidget)
from qt_material import apply_stylesheet

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

conversation_history = []

# Add a list of users and their content
users = [
    {
        "name": "Student",
        "content": "Please answer the question to the best of your abilities, make sure to give good detailed examples.",
    },
    {
        "name": "Software Engineer",
        "content": "Act as a senior software engineer and recommend the best solution to the problem and outline tradeoffs.",
    },
    {
        "name": "Designer",
        "content": "Act as a Designer and recommend the best solution to the problem and outline tradeoffs.",
    },
    {
        "name": "CFO",
        "content": "Act as a CFO and recommend the best solution to the problem and outline tradeoffs.",
    },
]

models = [
    {
        "name": "gpt-4",
        "id": "gpt-4"
    },
    {
        "name": "gpt-4-32k",
        "id": "gpt-4-32k"
    },
    {
        "name": "gpt-3.5-turbo",
        "id": "gpt-3.5-turbo"
    },
]

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

class MainWindow(QWidget):
    update_output_signal = Signal(str)
    cancelled_signal = Signal(bool)
    progress_signal = Signal(int)
    cancelled = False

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.update_output_signal.connect(self.update_output)
        self.cancelled_signal.connect(self.set_cancelled)


    def update_output(self, text):
        self.output_field.setPlainText(text)
        self.output_field.moveCursor(QtGui.QTextCursor.End)

    def set_cancelled(self, cancelled):
        self.cancelled = cancelled

    def check_cancelled(self):
        return self.cancelled

def main():
    conversation_id = get_conversation_id()

    app = QApplication(sys.argv)

    loop = qasync.QEventLoop(app)

    # styling
    # apply_stylesheet(app, theme="dark_blue.xml")
    default_font = QFont("Arial", 20)  # Change "12" to your desired font size
    app.setFont(default_font)

    # Create the main window
    window = MainWindow()
    window.setWindowTitle("ChatGPT Desktop Client")

    # Create the input field
    window.input_field = QTextEdit()
    window.input_field.setPlaceholderText("Enter your prompt here")
    window.input_field.setFont(default_font)

    # Create the generate button
    generate_button = QPushButton("Generate")

    # Create a stop button
    stop_button = QPushButton("Stop")
    stop_button.hide()

    # Create a clear button
    clear_button = QPushButton("Clear")

    # Create a label for the output field
    output_label = QLabel("Generated text:")

    # Create the output field
    window.output_field = QTextEdit()
    window.output_field.setReadOnly(True)
    default_font.setPointSize(default_font.pointSize() + 2)
    window.output_field.setFont(default_font)

    # Set the size policy
    sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
    window.output_field.setSizePolicy(sizePolicy)

    # Create a progress bar
    progress_bar = QProgressBar()
    progress_bar.setRange(0, 100)
    progress_bar.hide()
    window.progress_signal.connect(progress_bar.setValue)

    # Create a dropdown menu for selecting a system user
    user_dropdown = QComboBox()
    for user in users:
        user_dropdown.addItem(user["name"])

    # model selection
    model_dropdown = QComboBox()
    for model in models:
        model_dropdown.addItem(model["name"])

    def select_model(model_dropdown):
        selected_model = models[model_dropdown.currentIndex()]
        model = selected_model["id"]

    def select_user(user_dropdown):
        selected_user = users[user_dropdown.currentIndex()]

        # window.input_field.setPlainText(selected_user["content"])

    user_dropdown.currentIndexChanged.connect(lambda: select_user(user_dropdown))
    model_dropdown.currentIndexChanged.connect(lambda: select_model(model_dropdown))


    selected_user = users[user_dropdown.currentIndex()]
    selected_model = models[model_dropdown.currentIndex()]

    # The Open AI stuff
    openai.api_key = os.getenv("OPENAI_API_KEY")
    chat_mode = os.getenv("CHAT_MODE") == "true"


    def generate_text():
        global generate_text_task
        progress_bar.setValue(0)
        progress_bar.show()
        generate_text_task = asyncio.create_task(generate_text_async())

    async def generate_text_async():
        try:
            stop_button.show()
            question_text = window.input_field.toPlainText()
            prompt = get_prompt(question_text)
            progress_bar.show()
            progress_bar.setValue(50)
            model = models[model_dropdown.currentIndex()]['id']
            print(f"Using model {model}")
            core_function = functools.partial(
                openai.Completion.create,
                model=model,
                prompt=prompt,
                temperature=0,
                max_tokens=512,
                top_p=1,
            )
            if chat_mode:
                #  join the history in conversation so far and truncate the first 7000 characters
                context = ""
                for item in reversed(conversation_history):
                    context += f"{item['user']}: {item['text']}\n"
                context = context[:7000]+"\n\n"+question_text
                core_function = functools.partial(
                    openai.ChatCompletion.create,
                    messages=[
                        {"role": "system", "content": selected_user["content"]},
                        {"role": "user", "content": context+question_text},
                    ],
                    model=model,
                    temperature=0,
                    top_p=1,
                    stream=True,
                )
            response = await asyncio.get_event_loop().run_in_executor(None, core_function)
            generated_text = ""
            last_chunk = ""

            for chunk in response:
                cancelled = window.check_cancelled()
                if cancelled:
                    break
                if 'content' in chunk['choices'][0]['delta']:
                    new_chunk = chunk['choices'][0]['delta']['content']
                    generated_text += new_chunk
                    window.progress_signal.emit(50 + (len(generated_text) / 10))
                    current_text = window.output_field.toPlainText()
                    # output_field.setPlainText(generated_text)
                    window.update_output_signal.emit(generated_text)
                    QApplication.processEvents()
                    last_chunk = new_chunk
            generated_text = generated_text.strip()
            question_text = question_text.strip()
            conversation_history.append(create_conversation_item("HUMAN", question_text))
            conversation_history.append(create_conversation_item("AI", generated_text))
            # output_field.append(current_text + "\n---\n\n" + generated_text)
            progress_bar.setValue(100)
        except CancelledError:
            raise  # re-raise the exception to actually cancel the task
        except Exception as e:
            print(e)
            # output_field.append("Error: " + str(e))
            window.update_output_signal.emit("Error: " + str(e))
        finally:
            progress_bar.hide()
            stop_button.hide()
            window.cancelled_signal.emit(False)

    # Load your API key from an environment variable or secret management service
    generate_button.clicked.connect(generate_text)

    def stop_requesting():
        generate_text_task.cancel()
        window.cancelled_signal.emit(True)
        # Disconnect the generate button to stop requesting new text
        # generate_button.clicked.disconnect()

    stop_button.clicked.connect(stop_requesting)

    def clear_output():
        # reset conversation history
        conversation_history.clear()
        window.output_field.setText("")

    clear_button.clicked.connect(clear_output)

    # Create a clear input button
    clear_input_button = QPushButton("Clear Input")

    # Function to clear the input field
    def clear_input():
        window.input_field.setText("")

    clear_input_button.clicked.connect(clear_input)

    # dropdowns
    dropdown_layout = QHBoxLayout()
    dropdown_layout.addWidget(user_dropdown)
    dropdown_layout.addWidget(model_dropdown)

    # Core Buttons
    button_layout = QHBoxLayout()
    button_layout.addWidget(generate_button)
    button_layout.addWidget(clear_button)
    button_layout.addWidget(clear_input_button)

    # Create the layout
    layout = QVBoxLayout()
    layout.addLayout(dropdown_layout)
    layout.addWidget(window.input_field)
    layout.addLayout(button_layout)

    layout.addWidget(progress_bar)
    layout.addWidget(stop_button)
    layout.addWidget(output_label)
    layout.addWidget(window.output_field)

    # Set the layout for the main window
    window.setLayout(layout)

    # Set the default width and height for a desktop app in PySide
    window.setGeometry(100, 100, 800, 600)

    # Show the main window
    window.show()

    # Adjust heights
    window.output_field.setFixedHeight(1.5 * window.input_field.height())

    sys.exit(app.exec())


if __name__ == "__main__":
    print(main())
