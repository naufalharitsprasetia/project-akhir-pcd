## Install library in terminal
# pip install PyQt5 
# pip install opencv-python

# jalankan aplikasi dengan mengetik "python uaspcd.py" di terminal atau klik tombol run di vscode
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class ImageEnhancementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UAS PCD - Kelompok 1")
        self.setStyleSheet("background-color: #2e2e2e;")
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid #4b0082; padding: 5px;")
        
        self.load_button = QPushButton("Masukkan Gambar")
        self.save_button = QPushButton("Simpan Gambar")
        self.contrast_button = QPushButton("Peningkatan Kontras")
        self.sharpen_button = QPushButton("Peningkatan ketajaman (sharpening)")
        self.noise_button = QPushButton("Reduksi noise")
        self.brightness_button = QPushButton("Penyesuaian kecerahan dan warna")
        self.restore_button = QPushButton("Reset ke awal")
        self.restore_button.setEnabled(False)
        
        self.buttons = [self.load_button, self.save_button, self.contrast_button, self.sharpen_button, self.noise_button, self.brightness_button, self.restore_button]
        
        for button in self.buttons:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4b0082;
                    color: white;
                    border: 1px solid #4b0082;
                    padding: 10px;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                    transition: background-color 0.3s ease;
                }
                QPushButton:hover {
                    background-color: #6a0dad;
                }
                QPushButton:pressed {
                    background-color: #2e0854;
                }
                QPushButton:disabled {
                    background-color: #8a2be2;
                    border: 1px solid #8a2be2;
                }
            """)
            button.setFont(QFont("Arial", 12))
        
        self.load_button.clicked.connect(self.load_image)
        self.save_button.clicked.connect(self.save_image)
        self.contrast_button.clicked.connect(self.enhance_contrast)
        self.sharpen_button.clicked.connect(self.enhance_sharpening)
        self.noise_button.clicked.connect(self.reduce_noise)
        self.brightness_button.clicked.connect(self.adjust_brightness_contrast)
        self.restore_button.clicked.connect(self.restore_image)
        
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.contrast_button)
        layout.addWidget(self.sharpen_button)
        layout.addWidget(self.noise_button)
        layout.addWidget(self.brightness_button)
        layout.addWidget(self.restore_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.image = None
        self.original_image = None

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpeg *.jpg)")
        if file_name:
            self.image = cv2.imread(file_name)
            self.image = cv2.resize(self.image, (500, 500))  # Resize image to 500x500 pixels
            self.original_image = self.image.copy()
            self.display_image(self.image)
            self.enable_buttons(True)
            self.restore_button.setEnabled(False)

    def save_image(self):
        if self.image is not None:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image File", "", "Images (*.png *.jpeg *.jpg)")
            if file_name:
                cv2.imwrite(file_name, self.image)

    def enhance_contrast(self):
        if self.image is not None:
            enhanced_image = cv2.convertScaleAbs(self.image, alpha=1.5, beta=0)
            self.apply_enhancement(enhanced_image)

    def enhance_sharpening(self):
        if self.image is not None:
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
            enhanced_image = cv2.filter2D(src=self.image, ddepth=-1, kernel=kernel)
            self.apply_enhancement(enhanced_image)

    def reduce_noise(self):
        if self.image is not None:
            enhanced_image = cv2.fastNlMeansDenoisingColored(self.image, None, 10, 10, 7, 21)
            self.apply_enhancement(enhanced_image)

    def adjust_brightness_contrast(self):
        if self.image is not None:
            brightness = 64  # Default brightness value
            contrast = 1.3  # Default contrast value
            beta = brightness - 128
            enhanced_image = cv2.convertScaleAbs(self.image, alpha=contrast, beta=beta)
            self.apply_enhancement(enhanced_image)

    def apply_enhancement(self, enhanced_image):
        self.display_image(enhanced_image)
        self.image = enhanced_image
        self.enable_buttons(False)
        self.restore_button.setEnabled(True)

    def restore_image(self):
        if self.original_image is not None:
            self.image = self.original_image.copy()
            self.display_image(self.image)
            self.enable_buttons(True)
            self.restore_button.setEnabled(False)

    def enable_buttons(self, enable):
        self.contrast_button.setEnabled(enable)
        self.sharpen_button.setEnabled(enable)
        self.noise_button.setEnabled(enable)
        self.brightness_button.setEnabled(enable)

    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEnhancementApp()
    window.show()
    sys.exit(app.exec_())
