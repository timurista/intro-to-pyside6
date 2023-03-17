import asyncio
import functools
import os
import sys
from asyncio import CancelledError
from uuid import uuid4

import openai
import qasync
from dotenv import load_dotenv
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QProgressBar,
                               QPushButton, QTextEdit, QVBoxLayout, QWidget)
from qt_material import apply_stylesheet

load_dotenv()

conversation_history = []

def create_conversation_item(user_name, text):
    return {
        "user": user_name,
        "text": text
    }

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
    prompt += "HUMAN: "+text_to_send
    return prompt



def main():
    conversation_id = get_conversation_id()

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
    chat_mode = os.getenv("CHAT_MODE") == "true"
    model = "text-davinci-003"
    if chat_mode:
        model = os.getenv("OPENAI_MODEL")

    def generate_text():
        global generate_text_task
        progress_bar.setValue(0)
        progress_bar.show()
        generate_text_task = asyncio.create_task(generate_text_async())

    async def generate_text_async():
        try:
            stop_button.show()
            question_text = input_field.toPlainText()
            prompt = get_prompt(question_text)
            progress_bar.show()
            progress_bar.setValue(50)
            print(prompt)
            print("is chat mode", chat_mode)
            core_function = functools.partial(openai.Completion.create, model=model, prompt=prompt, temperature=0, max_tokens=512, top_p=1 )
            if chat_mode:
                core_function = functools.partial(openai.ChatCompletion.create, messages=[
                    {
                        "role": "system", "content": "Please answer the question to the best of your abilities, make sure to give good detailed examples."
                    },
                    {
                        "role": "user", "content": question_text
                    }
                ], model=model, temperature=0, top_p=1 )
            response = await asyncio.get_event_loop().run_in_executor(None, core_function)
            print(response)
            progress_bar.setValue(100)
            if chat_mode:
                generated_text = response["choices"][0]["message"]["content"]
            else:
                generated_text = response["choices"][0]["text"]
                # trim empty lines and spaces from generated_text
            generated_text = generated_text.strip()
            question_text = question_text.strip()
            current_text = output_field.toPlainText()
            conversation_history.append(create_conversation_item("HUMAN", question_text))
            conversation_history.append(create_conversation_item("AI", generated_text))
            output_field.append(current_text + "\n---\n\n" + generated_text)
        except CancelledError:
            pass
        except Exception as e:
            print(e)
            output_field.append("Error: " + str(e))
        finally:
            progress_bar.hide()
            stop_button.hide()

    # Load your API key from an environment variable or secret management service
    generate_button.clicked.connect(generate_text)

    def stop_requesting():
        generate_text_task.cancel()
        # Disconnect the generate button to stop requesting new text
        # generate_button.clicked.disconnect()

    stop_button.clicked.connect(stop_requesting)

    def clear_output():
        # reset conversation history
        conversation_history.clear()
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

if __name__ == '__main__':
    print(main())
