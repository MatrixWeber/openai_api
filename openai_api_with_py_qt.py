import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QScrollArea, QProgressBar)
from PyQt5 import QtCore
import openai
import os
from time import sleep

script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct a file path relative to the script directory
file_path = os.path.join(script_dir, 'api_keys.txt')

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'OpenAI API'
        self.left = 0
        self.top = 0
        self.width = 1920
        self.height = 1280
        self.initUI()
    
    def initUI(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()
        prompt_label = QLabel('Enter the prompt:', self)
        self.prompt_input = QLineEdit(self)
        file_name_label = QLabel('Enter the file name:', self)
        self.file_name_input = QLineEdit(self)
        self.file_name_input.setText(file_path)
        browse_button = QPushButton('Browse', self)
        browse_button.clicked.connect(self.browse_file)
        generate_text_button = QPushButton('Generate Text', self)
        generate_text_button.clicked.connect(self.generate_text)
        clear_output_button = QPushButton('Clear Output', self)
        clear_output_button.clicked.connect(self.clear_output)
        self.output_label = QLabel(self)
        self.output_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.output_label.setAlignment(QtCore.Qt.AlignTop)
        # Create a QScrollArea and set the QLabel as its widget
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.output_label)
        scroll_area.setWidgetResizable(True)  # Make the QLabel resizable with the QScrollArea
        hbox_browse = QHBoxLayout()
        hbox_browse.addWidget(self.file_name_input)
        hbox_browse.addWidget(browse_button)

        vbox = QVBoxLayout()
        vbox.addWidget(prompt_label)
        vbox.addWidget(self.prompt_input)
        vbox.addWidget(file_name_label)
        vbox.addLayout(hbox_browse)
        vbox.addWidget(generate_text_button)
        vbox.addWidget(scroll_area)
        vbox.addWidget(clear_output_button)
        vbox.addWidget(self.progress_bar)
        vbox.setStretch(5, 2)  # stretch the output_label widget
        self.setLayout(vbox)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            self.file_name_input.setText(file_name)

        
    def generate_text(self):
        self.progress_bar.show()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(50)
        prompt = self.prompt_input.text()
        file_name = self.file_name_input.text()

        with open(file_name, 'r') as f:
            openai.organization = f.readline().strip()
            openai.api_key = f.readline().strip()

        models = openai.Model.list()

        model_engine = "text-davinci-003"

        try:
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            data = completion.to_dict()
            choices = data['choices']
            first_choice = choices[0]
            text = first_choice['text']
            self.output_label.setText(text)
        finally:  # Reset the progress bar
            self.progress_bar.setValue(100)
            sleep(1)
            self.progress_bar.hide()

    
    def clear_output(self):
        self.output_label.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
