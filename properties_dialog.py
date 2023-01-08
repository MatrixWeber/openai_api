from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFileDialog, QLabel, QSlider)
from PyQt5 import QtCore

class PropertiesDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PyQt5 File Dialog')
        self.resize(640, 480)

        creativity_label = QLabel('Enter Creativity:', self)

        slider = QSlider(QtCore.Qt.Horizontal, self)
        slider.move(60, 60)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(10)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(1)
        hbox = QHBoxLayout()
        hbox.addWidget(creativity_label)
        hbox.addWidget(slider)
        hbox.addStretch(1)
        hbox.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(hbox)

    def show_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')