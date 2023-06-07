from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLCDNumber, QLineEdit, QGridLayout, QWidget, QAbstractButton, QPushButton, QLabel, QListView, QComboBox, QTextEdit, QSlider , QGroupBox
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QImage, QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt, QPoint, QRect, QAbstractListModel, QModelIndex, QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import sketch
import sys
import requests
import json
from PIL import Image
from io import BytesIO
import os, io
#import config
import replicate
#from CanvasWidget import CanvasWidget

#os.environ["REPLICATE_API_TOKEN"] = config.replicate_api_key
#API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V1.4"
#headers = {"Authorization": f"Bearer {config.huggingface_api_key}"}
#os.makedirs('chatbot_responses', exist_ok=True)
#os.makedirs('bookmarks', exist_ok=True)
#os.makedirs('controlnet_responses', exist_ok=True)

class Pallete(QGroupBox):
    def __init__(self):
        super().__init__("pallete")
        self.Erasing = QPushButton("Erase Mode")
        self.bookMarkSendFromCanvas = QPushButton("Book Mark")
        self.PixelThicknessSliderForPallete = QSlider()
        self.PixelOpaquenessSliderForPallete = QSlider()
        self.PixelThicknessSliderForPallete.setOrientation(Qt.Horizontal)  # Set the slider orientation to horizontal
        self.PixelThicknessSliderForPallete.setFixedSize(100, 20)
        self.PixelOpaquenessSliderForPallete.setOrientation(Qt.Horizontal)  # Set the slider orientation to horizontal
        self.PixelOpaquenessSliderForPallete.setFixedSize(100, 20)
        self.PixelThicknessValueForPallete = QLCDNumber()
        self.PixelThicknessValueForPallete.setFixedSize(50, 20)
        self.PixelOpaquenessValueForPallete = QLCDNumber()
        self.PixelOpaquenessValueForPallete.setFixedSize(50, 20)

        palleteLayout = QGridLayout(self)
        palleteLayout.addWidget(self.Erasing, 0, 0)
        palleteLayout.addWidget(self.bookMarkSendFromCanvas, 1, 0)
        palleteLayout.addWidget(self.PixelThicknessSliderForPallete, 0, 1)
        palleteLayout.addWidget(self.PixelOpaquenessSliderForPallete, 1, 1)
        palleteLayout.addWidget(self.PixelThicknessValueForPallete, 0, 2)
        palleteLayout.addWidget(self.PixelOpaquenessValueForPallete, 1, 2)