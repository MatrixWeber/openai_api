import sys
from PyQt5.QtWidgets import (QMainWindow, QMenuBar, QAction, QMenu, QTextEdit, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QScrollArea, QProgressBar, QListWidget, QDockWidget)
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
import openai
import os
from time import sleep
import properties_dialog

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
        self.list_widget = QListWidget()
        self.list_widget.clicked.connect(self.handleItemClicked)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()
        prompt_label = QLabel('Enter the prompt:', self)
        self.prompt_input = QTextEdit(self)
        self.prompt_input.setFixedHeight(200)
        self.prompt_input.setAlignment(QtCore.Qt.AlignTop)
        self.prompt_input.setStyleSheet("background-color: black; color: white;")
        self.prompt_input.setAcceptRichText(True)
        # self.prompt_input.setTabChangesFocus(True)
        file_name_label = QLabel('Enter the file name:', self)
        # self.file_name_input = QLineEdit(self)
        # self.file_name_input.setText(file_path)
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
        # scroll_area.setFixedHeight(800)  # Set a fixed height for the QScrollArea
        # hbox_browse = QHBoxLayout()
        # hbox_browse.addWidget(self.file_name_input)

        vbox = QVBoxLayout()
        vbox.addWidget(prompt_label)
        vbox.addWidget(self.prompt_input)
        vbox2 = QVBoxLayout()
        vbox2.addLayout(vbox)
        vbox2.addWidget(file_name_label)
        # vbox2.addLayout(hbox_browse)
        vbox2.addWidget(generate_text_button)
        vbox2.addWidget(scroll_area)
        vbox2.addWidget(clear_output_button)
        vbox2.addWidget(self.progress_bar)
        vbox2.setStretch(3, 2)  # stretch the output_label widget
        hbox = QHBoxLayout()
        hbox.addLayout(vbox2)
        hbox.addWidget(self.list_widget)


        # Menubar
        menubar = QMenuBar()
        # Create a QMenu and add it to the QMenuBar
        fileMenu = menubar.addMenu('File')
        # Create a QAction and add it to the QMenu
        openFile = QAction('Open Api Key', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.browse_file)
        fileMenu.addAction(openFile)

                # Create a QMenu and add it to the QMenuBar
        propertiesMenu = menubar.addMenu('Einstellungen')
        # Create a QAction and add it to the QMenu
        changeProperty = QAction('Ändern', self)
        changeProperty.setShortcut('Ctrl+E')
        changeProperty.triggered.connect(self.properties_dialog)
        propertiesMenu.addAction(changeProperty)
        # Add the QMenuBar to the QWidget layout
        hbox.setMenuBar(menubar)
        self.setLayout(hbox)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
             file_path = file_name

    def properties_dialog(self):
        self.myDialog = properties_dialog.PropertiesDialog()
        self.myDialog.show()

    def handleItemClicked(self):
        # Do something with the clicked item here
        selected_items = self.list_widget.currentItem()
        if selected_items is not None:
            item_text = selected_items.text()
            self.prompt_input.setText(item_text)
        
    def generate_text(self):
        self.progress_bar.show()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(50)
        prompt = self.prompt_input.toPlainText()
        # file_name = self.file_name_input.text()

        with open(file_path, 'r') as f:
            openai.organization = f.readline().strip()
            openai.api_key = f.readline().strip()

        models = openai.Model.list()

        model_engine = "text-davinci-003"

        try:
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=2048,
                temperature=0.9,
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
            self.list_widget.insertItem(0, prompt)
        finally:  # Reset the progress bar
            self.progress_bar.setValue(100)
            sleep(1)
            self.progress_bar.hide()

    
    def clear_output(self):
        self.output_label.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.setStyleSheet("font-size: 20px;")
    ex.show()
    sys.exit(app.exec_())
