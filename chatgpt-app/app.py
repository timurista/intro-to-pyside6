import asyncio
import base64
import functools
import gzip
import json
import os
import re
import sys
from asyncio import CancelledError
from uuid import uuid4

import openai
import PySide6.QtGui as QtGui
import qasync
from dotenv import load_dotenv
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog,
                               QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMessageBox, QProgressBar, QPushButton,
                               QScrollArea, QSizePolicy, QTextEdit,
                               QVBoxLayout, QWidget)
from qt_material import apply_stylesheet

from personas import users
from textcompressor import CodeTextCompressor
from token_calculator import TokenCalculator

compressor = CodeTextCompressor()
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

conversation_history = []



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
    prompt += "ME: " + text_to_send
    return prompt

class MainWindow(QWidget):
    update_output_signal = Signal(str)
    cancelled_signal = Signal(bool)
    progress_signal = Signal(int)
    cancelled = False

    def __init__(self, *args, **kwargs):
        global models
        super(MainWindow, self).__init__(*args, **kwargs)
        self.update_output_signal.connect(self.update_output)
        self.cancelled_signal.connect(self.set_cancelled)
        openai.api_key = os.getenv("OPENAI_API_KEY")
        try:
            print("Finding Models")
            # print(openai.Model.list())
            models = [ d['id'] for d in openai.Model.list()['data'] if 'id' in d and d['id'] is not None and d['id'].startswith('gpt-')]

            models = [{'name': m, 'id': m} for m in models]
            # if the model doesn't have -06 after it then add -9999
            for m in models:
                # use regex to find gpt-4-{1...9}*
                if not re.search(r'gpt-4-[1-9]', m['name']):
                    m['name'] = m['name'] + '-X'
            # sort reversed so that gpt-4 is first
            models.sort(key=lambda x: x['name'], reverse=True)
            # remove the -X from the name
            for m in models:
                m['name'] = m['name'].replace('-X', '')

            print(f"found {len(models)} models")

        except Exception as e:
            print("Error Finding Models ", e)
            self.models = models


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

    def save_state():
        state = {
            "conversation_history": conversation_history,
            "selected_model": selected_model,
            "selected_user": selected_user
        }
        with open('state.json', 'w') as f:
            json.dump(state, f)
    def load_state():
        global conversation_history, selected_model, selected_user
        try:
            with open('state.json', 'r') as f:
                state = json.load(f)
                conversation_history = state["conversation_history"]
                selected_model = state["selected_model"]
                selected_user = state["selected_user"]
        except FileNotFoundError:
            # If the file doesn't exist, initialize with default values
            conversation_history = []
            selected_model = models[0]
            selected_user = users[0]

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

    # Set the size policy
    input_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    window.input_field.setSizePolicy(input_size_policy)

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
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    window.output_field.setSizePolicy(sizePolicy)

    # Create a progress bar
    progress_bar = QProgressBar()
    progress_bar.setRange(0, 100)
    progress_bar.show()
    window.progress_signal.connect(progress_bar.setValue)
    token_calculator = TokenCalculator()
    token_calculator.progress_signal.connect(progress_bar.setValue)

    #  size policy for the progress bar
    progress_bar_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    progress_bar.setSizePolicy(progress_bar_size_policy)

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
        global selected_user
        selected_user = users[user_dropdown.currentIndex()]

        # window.input_field.setPlainText(selected_user["content"])

    def get_selected_user():
        return users[user_dropdown.currentIndex()]

    user_dropdown.currentIndexChanged.connect(lambda: select_user(user_dropdown))
    model_dropdown.currentIndexChanged.connect(lambda: select_model(model_dropdown))


    selected_user = users[user_dropdown.currentIndex()]
    selected_model = models[model_dropdown.currentIndex()]

    # The Open AI stuff

    chat_mode = os.getenv("CHAT_MODE") != "false"

    # Add a button for file upload
    upload_button = QPushButton("Upload File")

    uploaded_files = []

    def upload_file():
        # Open a file dialog and get the selected file path
        file_path, _ = QFileDialog.getOpenFileName()

        # Read the file
        with open(file_path, 'r') as f:
            file_content = f.read().strip()

        # Add the compressed content to the conversation history
        filename = os.path.basename(file_path)
        compressedFileContents = compressor.generate_prompt(file_content)
        original_size, new_size = compressor.compare_lengths(file_content, compressedFileContents)
        reduction = (original_size - new_size) / original_size * 100

        print(f"Reduction {reduction:.2f}% {original_size} -> {new_size}")
        if new_size > original_size:
            conversation_history.append(create_conversation_item("ME", f'COMPRESS the file: {filename} and use it to answer my question. Here is file contents: ```{file_content}```'))
        else:
            conversation_history.append(create_conversation_item("ME", f'READ the file: {filename} and use it to answer my question. Here is file contents: ```{compressedFileContents}```'))
        tokens = calculate_tokens()
        token_calculator.calculate_and_emit(tokens)
         # Add the file path to the uploaded_files list
        uploaded_files.append(file_path)

        # Update the file bar
        update_file_bar()

    upload_button.clicked.connect(upload_file)

    # Create the file bar
    file_bar = QHBoxLayout()

    def clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def remove_filename_from_history(filename):
        for item in conversation_history:
            if item["text"].find(f"file: {filename}") != -1:
                conversation_history.remove(item)

    def update_file_bar():
        # Clear the file bar
        clear_layout(file_bar)

        # Add a QPushButton for each file in the uploaded_files list
        for file_path in uploaded_files:
            # Create a QPushButton with the file name
            file_name = os.path.basename(file_path)
            file_button = QPushButton(file_name)

            def on_file_button_clicked():
                print("clicked on file button", file_path, "uploaded files", uploaded_files)
                if file_path in uploaded_files:
                    uploaded_files.remove(file_path)
                    filename = os.path.basename(file_path)
                    remove_filename_from_history(filename)
                    # and remove it from conver
                    update_file_bar()
                    tokens = calculate_tokens()
                    token_calculator.calculate_and_emit(tokens)



            # Connect the QPushButton's clicked signal to a lambda function that removes the file from the uploaded_files list and updates the file bar
            # file_button.clicked.connect(lambda: uploaded_files.remove(file_path) and update_file_bar())
            file_button.clicked.connect(on_file_button_clicked)

            # Add the QPushButton to the file bar
            file_bar.addWidget(file_button)


    def generate_text():
        global generate_text_task
        # progress_bar.setValue(0)
        progress_bar.show()
        generate_text_task = asyncio.create_task(generate_text_async())

    async def generate_text_async():
        try:
            stop_button.show()
            question_text = window.input_field.toPlainText()
            prompt = get_prompt(question_text)
            # progress_bar.show()
            model = models[model_dropdown.currentIndex()]['id']
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
                selected_user = get_selected_user()
                print("system user", selected_user["content"])
                core_function = functools.partial(
                    openai.ChatCompletion.create,
                    messages=[
                        {"role": "system", "content": selected_user["content"]},
                        {"role": "user", "content": context+"\nHUMAN: " + question_text},
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
                    # window.progress_signal.emit(50 + (len(generated_text) / 10))
                    tokens = calculate_tokens() + len(generated_text.split())
                    token_calculator.calculate_and_emit(tokens)
                    current_text = window.output_field.toPlainText()
                    # output_field.setPlainText(generated_text)
                    window.update_output_signal.emit(generated_text)
                    QApplication.processEvents()
                    last_chunk = new_chunk
            generated_text = generated_text.strip()
            question_text = question_text.strip()
            conversation_history.append(create_conversation_item("HUMAN", question_text))
            conversation_history.append(create_conversation_item("AI", generated_text))
        except CancelledError:
            raise  # re-raise the exception to actually cancel the task
        except Exception as e:
            print(e)
            # output_field.append("Error: " + str(e))
            window.update_output_signal.emit("Error: " + str(e))
        finally:
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

        for file in uploaded_files:
            filename = os.path.basename(file)
            remove_filename_from_history(filename)

        uploaded_files.clear()
        clear_layout(file_bar)
        window.output_field.setText("")
        window.progress_signal.emit(0)

    clear_button.clicked.connect(clear_output)

    # Create a clear input button
    clear_input_button = QPushButton("Clear Input")

    # Function to clear the input field
    def clear_input():
        window.input_field.setText("")

    clear_input_button.clicked.connect(clear_input)

    # Function to calculate the number of tokens used so far
    def calculate_tokens():
        total_tokens = sum(len(item["text"].split()) for item in conversation_history)
        return total_tokens

    progress_label = QLabel("Tokens used so far:")


    # SHow history button
    show_history_button = QPushButton("Show History")
    def show_history():
        history_text = "\n".join([f"{item['user']}: {item['text']}" for item in conversation_history])

        # Create a QDialog
        dialog = QDialog()

        # Create a QTextEdit and set the history text
        text_edit = QTextEdit()
        text_edit.setPlainText(history_text)

        # Create a QScrollArea and set the QTextEdit as its widget
        scroll = QScrollArea()
        scroll.setWidget(text_edit)
        scroll.setWidgetResizable(True)

        # Create a QVBoxLayout and add the QScrollArea
        layout = QVBoxLayout(dialog)
        layout.addWidget(scroll)

        # Set the QDialog layout and show the QDialog
        dialog.setLayout(layout)
        dialog.setWindowTitle("Conversation History")
        dialog.resize(500, 800)
        dialog.exec()
    show_history_button.clicked.connect(show_history)

    # dropdowns
    dropdown_layout = QHBoxLayout()
    dropdown_layout.addWidget(user_dropdown)
    dropdown_layout.addWidget(model_dropdown)

    # Core Buttons
    button_layout = QHBoxLayout()
    button_layout.addWidget(generate_button)
    button_layout.addWidget(clear_button)
    button_layout.addWidget(clear_input_button)
    button_layout.addWidget(upload_button)
    button_layout.addWidget(show_history_button)

    # Create the layout
    layout = QVBoxLayout()

    top_layout = QVBoxLayout()
    top_layout.addLayout(dropdown_layout)
    top_layout.addWidget(window.input_field, 1)
    top_layout.addLayout(button_layout, 1)
    top_layout.addLayout(file_bar, 1)

    top_layout.addWidget(progress_label)
    top_layout.addWidget(progress_bar, 1)
    top_layout.addWidget(stop_button, 1)

    bottom_layout = QVBoxLayout()
    bottom_layout.addWidget(output_label)  # Place output_label at row 0, column 0
    bottom_layout.addWidget(window.output_field)  # Place window.output_field at row 1, column 0


    layout.addLayout(top_layout)
    layout.addLayout(bottom_layout)


    # Set the layout for the main window
    window.setLayout(layout)

    # Set the default width and height for a desktop app in PySide
    window.setGeometry(100, 100, 800, 600)

    # Show the main window
    window.show()

    # Adjust heights
    # window.output_field

    sys.exit(app.exec())

if __name__ == "__main__":
    print(main())
