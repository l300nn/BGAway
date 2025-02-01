import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout
from rembg import remove
from PIL import Image
import io

class BackgroundRemoverApp(QWidget):
    def __init__(self):
        super().__init__()
    self.initUI()

    def __initUI(self):
        self.setWindowTitle("BGAway")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Upload a image:", self)
        self.button_select = QPushButton("Choose image", self)
        self.button_remove_bg = QPushButton("Remove background", self)

        self.button_select.clicked.connect(self.loadImage)
        self.button_remove_bg.clicked.connect(self.removeBackground)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_select)
        layout.addWidget(self.button_remove_bg)

        self.setLayout(layout)
        self.image_path = ""
