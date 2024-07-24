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

# jalankan aplikasi dengan mengetik "python coba.py" di terminal

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2 # OpenCV
import numpy as np

class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("UAS PCD - Naufal, Def, Pangestu")
        self.setGeometry(100, 100, 800, 600)
        
        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setFixedSize(400, 400)  # Set fixed size for the image display
        
        self.resultLabel = QLabel(self)
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel.setFixedSize(400, 400)  # Set fixed size for the result display
        
        self.openButton = QPushButton("Open Image", self)
        self.openButton.clicked.connect(self.open_image)
        
        self.grayButton = QPushButton("Convert to Grayscale", self)
        self.grayButton.clicked.connect(self.convert_to_grayscale)
        
        # Layout for buttons on the left
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.openButton)
        buttonLayout.addWidget(self.grayButton)
        buttonLayout.addStretch()  # Adds a stretchable space to push buttons to the top
        
        # Layout for images on the right
        imageLayout = QVBoxLayout()
        imageLayout.addWidget(self.imageLabel)
        imageLayout.addWidget(self.resultLabel)
        
        # Main layout
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(imageLayout)
        
        container = QWidget()
        container.setLayout(mainLayout)
        
        self.setCentralWidget(container)
        
        self.image = None
    
    def open_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            self.image = cv2.imread(fileName)
            self.display_image(self.image, self.imageLabel)
    
    def display_image(self, image, label):
        # Resize image to fit the label size
        h, w = label.height(), label.width()
        resized_image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)
        
        qformat = QImage.Format_Indexed8
        if len(resized_image.shape) == 3:
            if resized_image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(resized_image, resized_image.shape[1], resized_image.shape[0], resized_image.strides[0], qformat)
        img = img.rgbSwapped()
        label.setPixmap(QPixmap.fromImage(img))
    
    def convert_to_grayscale(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.display_image(gray_image, self.resultLabel)

app = QApplication(sys.argv)
window = ImageProcessingApp()
window.show()
sys.exit(app.exec_())
