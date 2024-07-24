# **Tujuan**Mengembangkan aplikasi desktop sederhana menggunakan Python yang mampu melakukan peningkatan kualitas gambar (image enhancement) dengan berbagai teknik.

# **Deskripsi Proyek**Mahasiswa diminta untuk membuat aplikasi desktop yang dapat melakukan beberapa fungsi peningkatan kualitas gambar seperti:

# 1. Peningkatan kontras
# 2. Peningkatan ketajaman (sharpening)
# 3. Reduksi noise
# 4. Penyesuaian kecerahan dan warna

# **Spesifikasi Proyek**1. **Bahasa Pemrograman**: Python
# 2. **Framework**: PyQt atau Tkinter untuk GUI
# 3. **Library Image Processing**: OpenCV
# 4. **Fitur Utama**:
# - Antarmuka pengguna (GUI) yang intuitif dan mudah digunakan.
# - Fungsi untuk memuat dan menyimpan gambar.
# - Opsi untuk menerapkan berbagai teknik peningkatan kualitas gambar.
# - Pratinjau hasil sebelum menyimpan.
# 5. **Dokumentasi**:
# - Dokumentasi kode yang baik (komentar, docstrings).
# - Tautan Github project
# - Laporan proyek yang menjelaskan teknik yang digunakan, bagaimana aplikasi bekerja, dan hasil uji coba



## Install library in terminal
# pip install PyQt5 
# pip install opencv-python

# jalankan aplikasi dengan mengetik "python uaspcd.py" di terminal
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class ImageEnhancementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Enhancement App")
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        
        self.save_button = QPushButton("Save Image")
        self.save_button.clicked.connect(self.save_image)
        
        self.contrast_button = QPushButton("Enhance Contrast")
        self.contrast_button.clicked.connect(self.enhance_contrast)
        
        self.sharpen_button = QPushButton("Enhance Sharpening")
        self.sharpen_button.clicked.connect(self.enhance_sharpening)
        
        self.noise_button = QPushButton("Reduce Noise")
        self.noise_button.clicked.connect(self.reduce_noise)
        
        self.brightness_button = QPushButton("Adjust Brightness/Contrast")
        self.brightness_button.clicked.connect(self.adjust_brightness_contrast)
        
        self.restore_button = QPushButton("Restore")
        self.restore_button.clicked.connect(self.restore_image)
        self.restore_button.setEnabled(False)
        
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
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg)")
        if file_name:
            self.image = cv2.imread(file_name)
            self.original_image = self.image.copy()
            self.display_image(self.image)
            self.enable_buttons(True)
            self.restore_button.setEnabled(False)

    def save_image(self):
        if self.image is not None:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image File", "", "Images (*.png *.xpm *.jpg)")
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
