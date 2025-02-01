import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout
from rembg import remove
from PIL import Image
import io
import sys
import subprocess

required_packages = ["rembg", "PyQt6", "Pillow"]

def install_missing_packages():
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} nicht gefunden. Installiere...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

class BackgroundRemoverApp(QWidget): 
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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

    def loadImage(self):
        file_dialog =QFileDialog
        file_path, _ = file_dialog.getOpenFileName(self, "Open image", "", "Image (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            self.label.setText(f"Image: {file_path}")

    def removeBackground(self):
        if self.image_path:
            input_image = Image.open(self.image_path)
            output_image = remove(input_image)

            save_path, _ =  QFileDialog.getSaveFileName(self, "Save under", "output.png","PNG-file (*.png)")
            if save_path:
                output_image.save(save_path)
                self.label.setText("Background removed and image saved!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BackgroundRemoverApp()  
    window.show()
    sys.exit(app.exec())    