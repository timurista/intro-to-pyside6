import asyncio
import functools
import os
import sys
from asyncio import CancelledError
from uuid import uuid4

import openai
import qasync
from dotenv import load_dotenv
from PySide6.QtCore import Qt
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

class QInputField(QTextEdit):
    def keyPressEvent(self, event):
        # command + enter
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Return:
            self.generate_text()
        else:
            super().keyPressEvent(event)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.generate_text_task = None
        self.setWindowTitle("ChatGPT Desktop Client")

        # Create the input field
        self.input_field = QInputField()
        self.input_field.setPlaceholderText("Enter your prompt here")
        self.input_field.generate_text = self.generate_text

        # Create the generate button
        self.generate_button = QPushButton("Generate")

        # Create a stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.hide()

        # Create a clear button
        self.clear_button = QPushButton("Clear")

        # Create a label for the output field
        self.output_label = QLabel("Generated text:")

        # Create the output field
        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)

        # Create a progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.hide()

        # The Open AI stuff
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Create a layout and add the input field, generate button, stop button, clear button, output label, and output field
        layout = QVBoxLayout()
        layout.addWidget(self.input_field)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_field)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
        self.setGeometry(100, 100, 800, 600)


        # Connect the generate button to the generate_text function
        self.generate_button.clicked.connect(self.generate_text)
        # Connect the stop button to the stop_text function
        self.stop_button.clicked.connect(self.stop_text)
        # Connect the clear button to the clear_text function
        self.clear_button.clicked.connect(self.clear_text)

    def generate_text(self):
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.generate_text_task = asyncio.create_task(self.generate_text_async())

    def stop_text(self):
        self.generate_text_task.cancel()

    def clear_text(self):
        self.output_field.clear()

    async def generate_text_async(self):
        try:
            self.stop_button.show()
            question_text = self.input_field.toPlainText()
            prompt = get_prompt(question_text)
            self.progress_bar.show()
            print(prompt)
            self.progress_bar.setValue(50)
            response = await asyncio.get_event_loop().run_in_executor(None, functools.partial(openai.Completion.create, model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=512, top_p=1 ))
            print(response)
            self.progress_bar.setValue(100)
            generated_text = response["choices"][0]["text"]
            # trim empty lines and spaces from generated_text
            generated_text = generated_text.strip(" \n")
            question_text = question_text.strip()
            current_text = self.output_field.toPlainText()
            conversation_history.append(create_conversation_item("HUMAN", question_text))
            conversation_history.append(create_conversation_item("AI", generated_text))
            self.output_field.append(current_text + "\n---\n\n" + generated_text)
        except CancelledError:
            pass
        except Exception as e:
            print(e)
            self.output_field.append("Error: " + str(e))
        finally:
            self.progress_bar.setValue(100)
            # wait 1 second before hiding the progress bar
            await asyncio.sleep(1)
            self.progress_bar.hide()
            self.stop_button.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_blue.xml")

    # needed for qasync
    app.processEvents()
    loop = qasync.QEventLoop(app)

    # close the event loop when the app closes
    app.aboutToQuit.connect(loop.close)

    window = MainWindow()
    pixmap = QPixmap("splash.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    window.show()
    splash.finish(window)
    sys.exit(app.exec())


# def main():

#     app = QApplication(sys.argv)
#     pixmap = QPixmap("splash.png")
#     splash = QSplashScreen(pixmap)
#     splash.show()
#     app.processEvents()
#     loop = qasync.QEventLoop(app)

#     # styling
#     apply_stylesheet(app, theme="dark_blue.xml")

#     # Create the main window
#     window = QWidget()
#     window.setWindowTitle("ChatGPT Desktop Client")


#     # Create the input field
#     input_field = QInputField()
#     input_field.setPlaceholderText("Enter your prompt here")

#     # Create the generate button
#     generate_button = QPushButton("Generate")

#     # Create a stop button
#     stop_button = QPushButton("Stop")
#     stop_button.hide()

#     # Create a clear button
#     clear_button = QPushButton("Clear")

#     # Create a label for the output field
#     output_label = QLabel("Generated text:")

#     # Create the output field
#     output_field = QTextEdit()
#     output_field.setReadOnly(True)

#     # Create a progress bar
#     progress_bar = QProgressBar()
#     progress_bar.setRange(0, 100)
#     progress_bar.hide()

#     # The Open AI stuff
#     openai.api_key = os.getenv("OPENAI_API_KEY")

#     def generate_text():
#         global generate_text_task
#         progress_bar.setValue(0)
#         progress_bar.show()
#         generate_text_task = asyncio.create_task(generate_text_async())

#     async def generate_text_async():
#         try:
#             stop_button.show()
#             question_text = input_field.toPlainText()
#             prompt = get_prompt(question_text)
#             progress_bar.show()
#             print(prompt)
#             response = await asyncio.get_event_loop().run_in_executor(None, functools.partial(openai.Completion.create, model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=512, top_p=1 ))
#             print(response)
#             progress_bar.setValue(100)
#             generated_text = response["choices"][0]["text"]
#             # trim empty lines and spaces from generated_text
#             generated_text = generated_text.strip(" \n")
#             question_text = question_text.strip()
#             current_text = output_field.toPlainText()
#             conversation_history.append(create_conversation_item("HUMAN", question_text))
#             conversation_history.append(create_conversation_item("AI", generated_text))
#             output_field.append(current_text + "\n---\n\n" + generated_text)
#         except CancelledError:
#             pass
#         except Exception as e:
#             print(e)
#             output_field.append("Error: " + str(e))
#         finally:
#             progress_bar.hide()
#             stop_button.hide()

#     # Load your API key from an environment variable or secret management service
#     generate_button.clicked.connect(generate_text)

#     input_field.generate_text = generate_text


#     def stop_requesting():
#         generate_text_task.cancel()
#         # Disconnect the generate button to stop requesting new text
#         # generate_button.clicked.disconnect()

#     stop_button.clicked.connect(stop_requesting)

#     def clear_output():
#         # reset conversation history
#         conversation_history.clear()
#         output_field.setText("")

#     clear_button.clicked.connect(clear_output)

#     # Create the layout
#     layout = QVBoxLayout()
#     layout.addWidget(input_field)
#     layout.addWidget(generate_button)
#     layout.addWidget(progress_bar)
#     layout.addWidget(stop_button)
#     layout.addWidget(clear_button)
#     layout.addWidget(output_label)
#     layout.addWidget(output_field)


#     # Set the layout for the main window
#     window.setLayout(layout)

#     # Set the default width and height for a desktop app in PySide
#     window.setGeometry(100, 100, 800, 600)

#     # Show the main window
#     window.show()

#     splash.finish(window)

#     # with loop:
#     #     loop.run_forever()

#     sys.exit(app.exec())

# if __name__ == '__main__':
#     print(main())
