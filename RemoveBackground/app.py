import sys
import subprocess
import importlib.util
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QProgressBar
from rembg import remove
from PIL import Image
import onnxruntime
from PyQt6.QtCore import Qt, QThread, pyqtSignal

required_packages = ["rembg", "PyQt6", "Pillow", "onnxruntime"]
def install_missing_packages():
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            print(f"{package} not found. installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} sucessfully installed!")
install_missing_packages()


class BackgroundRemoverThread(QThread):
    progress = pyqtSignal(int) 
    finished = pyqtSignal(Image.Image)  

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self):
        try:
            input_image = Image.open(self.image_path)
         
            steps = 5  
            for i in range(1, steps + 1):
                self.progress.emit(i * (100 // steps))  
                self.msleep(500)  

            output_image = remove(input_image) 
            self.progress.emit(100)  
            self.finished.emit(output_image) 
        except Exception as e:
            print(f"Error: {e}")

class BackgroundRemoverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("BGAway")
        self.setGeometry(100, 100, 400, 250)

        self.label = QLabel("Select a image:", self)
        self.progress_bar = QProgressBar(self)  
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setValue(0)  

        self.button_select = QPushButton("Select image", self)
        self.button_remove_bg = QPushButton("remove background", self)

        self.button_select.clicked.connect(self.loadImage)
        self.button_remove_bg.clicked.connect(self.startBackgroundRemoval)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)  
        layout.addWidget(self.button_select)
        layout.addWidget(self.button_remove_bg)

        self.setLayout(layout)
        self.image_path = ""

    def loadImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open image", "", "Bilder (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            self.label.setText(f"Image loaded: {file_path}")

    def startBackgroundRemoval(self):
        if self.image_path:
            self.progress_bar.setValue(0)  
            self.thread = BackgroundRemoverThread(self.image_path)
            self.thread.progress.connect(self.progress_bar.setValue)  
            self.thread.finished.connect(self.saveImage) 
            self.thread.start()

    def saveImage(self, output_image):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save under", "output.png", "PNG-Dateien (*.png)")
        if save_path:
            output_image.save(save_path)
            self.label.setText("Background removed and saved!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BackgroundRemoverApp()
    window.show()
    sys.exit(app.exec())
