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
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                               QListWidget, QMenu, QProgressBar, QPushButton,
                               QSplashScreen, QSystemTrayIcon, QTextEdit,
                               QVBoxLayout, QWidget)
from qt_material import apply_stylesheet

from utils import create_conversation_item, get_prompt, prompt_engineering

load_dotenv()


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

        self.conversation_history = []

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



        # Create sidebar menu
        self.menu = QMenu()
        self.menu.addAction("Quit", self.close)

        # Create the sidebar
        self.sidebar = QListWidget()
        self.sidebar.addItem("Prompt Templates")
        self.sidebar.addItem("Conversation History")
        self.sidebar.addItem("Settings")

        # Create a layout and add the input field, generate button, stop button, clear button, output label, and output field
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.clear_button)
        self.layout.addWidget(self.output_label)
        self.layout.addWidget(self.output_field)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)
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
            prompt = get_prompt(question_text, self.conversation_history)
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
            self.conversation_history.append(create_conversation_item("HUMAN", question_text))
            self.conversation_history.append(create_conversation_item("AI", generated_text))
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
    app.setApplicationName("Chat Blast")

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

    #create the tray icon
    tray_icon = QSystemTrayIcon()
    app_icon = QIcon("icon.png")
    tray_icon.setIcon(app_icon)

    app.setWindowIcon(app_icon)

    #create the menu
    menu = QMenu()
    menu.addAction("Action 1")
    menu.addAction("Action 2")
    menu.addAction("Quit")

    #set the menu to the tray icon
    tray_icon.setContextMenu(menu)

    #show the tray icon
    tray_icon.show()


    sys.exit(app.exec())
