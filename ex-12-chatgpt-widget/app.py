import asyncio
import functools
import os
import sys
from asyncio import CancelledError

import openai
import qasync
from dotenv import load_dotenv
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QProgressBar,
                               QPushButton, QTextEdit, QVBoxLayout, QWidget)
from qt_material import apply_stylesheet

load_dotenv()

app = QApplication(sys.argv)
loop = qasync.QEventLoop(app)

# styling
apply_stylesheet(app, theme="dark_blue.xml")

# Create the main window
window = QWidget()
window.setWindowTitle("ChatGPT Desktop Client")


# Create the input field
input_field = QTextEdit()
input_field.setPlaceholderText("Enter your prompt here")

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
output_field = QTextEdit()
output_field.setReadOnly(True)

# Create a progress bar
progress_bar = QProgressBar()
progress_bar.setRange(0, 100)
progress_bar.hide()

# The Open AI stuff
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_text():
    global generate_text_task
    progress_bar.setValue(0)
    progress_bar.show()
    generate_text_task = asyncio.create_task(generate_text_async())

async def generate_text_async():
    try:
        stop_button.show()
        prompt = input_field.toPlainText()
        progress_bar.show()
        response = await asyncio.get_event_loop().run_in_executor(None, functools.partial(openai.Completion.create, model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=512))
        print(response)
        progress_bar.setValue(100)
        generated_text = response["choices"][0]["text"]
        current_text = output_field.toPlainText()
        output_field.append(current_text + generated_text)
    except CancelledError:
        pass
    finally:
        progress_bar.hide()
        stop_button.hide()

# Load your API key from an environment variable or secret management service
generate_button.clicked.connect(generate_text)

def stop_requesting():
    generate_text_task.cancel()
    # Disconnect the generate button to stop requesting new text
    generate_button.clicked.disconnect()


def clear_output():
    output_field.setText("")

clear_button.clicked.connect(clear_output)

# Create the layout
layout = QVBoxLayout()
layout.addWidget(input_field)
layout.addWidget(generate_button)
layout.addWidget(progress_bar)
layout.addWidget(stop_button)
layout.addWidget(clear_button)
layout.addWidget(output_label)
layout.addWidget(output_field)


# Set the layout for the main window
window.setLayout(layout)

# Set the default width and height for a desktop app in PySide
window.setGeometry(100, 100, 800, 600)

# Show the main window
window.show()

# with loop:
#     loop.run_forever()

sys.exit(app.exec())
