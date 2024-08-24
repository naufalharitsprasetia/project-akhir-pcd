## Install library in terminal
# pip install PyQt5 
# pip install opencv-python

# jalankan aplikasi dengan mengetik "python uaspcd.py" di terminal atau klik tombol run di vscode
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QGridLayout, QPushButton, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class ImageEnhancementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UAS PCD - Kelompok 1")
        self.setStyleSheet("background-color: #FFDAB9;")
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid #4b0082; padding: 5px;")
        
        # Define buttons
        self.load_button = QPushButton("Masukkan Gambar")
        self.save_button = QPushButton("Simpan Gambar")
        self.contrast_button = QPushButton("Peningkatan Kontras")
        self.sharpen_button = QPushButton("Peningkatan Ketajaman")
        self.noise_button = QPushButton("Reduksi Noise")
        self.brightness_button = QPushButton("Penyesuaian Kecerahan dan Warna")
        self.binary_button = QPushButton("Transformasi Citra Biner")
        self.negative_button = QPushButton("Transformasi Citra Negatif")
        self.power_law_button = QPushButton("Transformasi Power-law")
        self.log_transform_button = QPushButton("Transformasi Logaritmik")
        self.grayscale_button = QPushButton("Grayscale")
        self.blur_button = QPushButton("Image Blurring")
        self.edge_button = QPushButton("Edge Detection")
        self.restore_button = QPushButton("Reset ke Awal")
        self.restore_button.setEnabled(False)
        
        self.buttons = [
            self.load_button, self.save_button, self.contrast_button, self.sharpen_button,
            self.noise_button, self.brightness_button, self.binary_button, self.negative_button,
            self.power_law_button, self.log_transform_button, self.grayscale_button, self.blur_button,
            self.edge_button, self.restore_button
        ]
        
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
        
        # Connect buttons to their functions
        self.load_button.clicked.connect(self.load_image)
        self.save_button.clicked.connect(self.save_image)
        self.contrast_button.clicked.connect(self.enhance_contrast)
        self.sharpen_button.clicked.connect(self.enhance_sharpening)
        self.noise_button.clicked.connect(self.reduce_noise)
        self.brightness_button.clicked.connect(self.adjust_brightness_contrast)
        self.binary_button.clicked.connect(self.binary_transformation)
        self.negative_button.clicked.connect(self.negative_transformation)
        self.power_law_button.clicked.connect(self.power_law_transformation)
        self.log_transform_button.clicked.connect(self.logarithmic_transformation)
        self.grayscale_button.clicked.connect(self.grayscale_transformation)
        self.blur_button.clicked.connect(self.image_blurring)
        self.edge_button.clicked.connect(self.edge_detection)
        self.restore_button.clicked.connect(self.restore_image)
        
        # Create a grid layout and add buttons in two columns
        button_layout = QGridLayout()
        
        # Add buttons to the grid layout
        button_layout.addWidget(self.load_button, 0, 0)
        button_layout.addWidget(self.save_button, 0, 1)
        button_layout.addWidget(self.contrast_button, 1, 0)
        button_layout.addWidget(self.sharpen_button, 1, 1)
        button_layout.addWidget(self.noise_button, 2, 0)
        button_layout.addWidget(self.brightness_button, 2, 1)
        button_layout.addWidget(self.binary_button, 3, 0)
        button_layout.addWidget(self.negative_button, 3, 1)
        button_layout.addWidget(self.power_law_button, 4, 0)
        button_layout.addWidget(self.log_transform_button, 4, 1)
        button_layout.addWidget(self.grayscale_button, 5, 0)
        button_layout.addWidget(self.blur_button, 5, 1)
        button_layout.addWidget(self.edge_button, 6, 0)
        button_layout.addWidget(self.restore_button, 6, 1)
        
        # Create a main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(button_layout)  # Add the grid layout with buttons
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        self.image = None
        self.original_image = None

    # Define the transformation functions (same as before)
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

    def binary_transformation(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            _, binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            self.apply_enhancement(cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR))

    def negative_transformation(self):
        if self.image is not None:
            negative_image = cv2.bitwise_not(self.image)
            self.apply_enhancement(negative_image)

    def power_law_transformation(self):
        if self.image is not None:
            gamma = 2.0  # Example gamma value
            gamma_corrected = np.array(255 * (self.image / 255) ** gamma, dtype='uint8')
            self.apply_enhancement(gamma_corrected)

    def logarithmic_transformation(self):
        if self.image is not None:
            c = 255 / np.log(1 + np.max(self.image))
            log_image = c * (np.log(self.image + 1))
            log_image = np.array(log_image, dtype=np.uint8)
            self.apply_enhancement(log_image)

    def grayscale_transformation(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.apply_enhancement(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR))

    def image_blurring(self):
        if self.image is not None:
            blurred_image = cv2.GaussianBlur(self.image, (15, 15), 0)
            self.apply_enhancement(blurred_image)

    def edge_detection(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray_image, 100, 200)
            self.apply_enhancement(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))

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
        for button in self.buttons:
            if button != self.restore_button:  # Exclude restore button
                button.setEnabled(enable)

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
