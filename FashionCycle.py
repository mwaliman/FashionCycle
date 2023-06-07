from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLCDNumber, QLineEdit, QGridLayout, QWidget, QAbstractButton, QPushButton, QLabel, QListView, QComboBox, QTextEdit, QSlider , QGroupBox
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QImage, QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt, QPoint, QRect, QAbstractListModel, QModelIndex, QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
#import sketch
import sys
import requests
import json
from PIL import Image
from io import BytesIO
import os, io
#import config
import replicate
from fashion_cycle import FashionCycle
#from CanvasWidget import CanvasWidget

#os.environ["REPLICATE_API_TOKEN"] = config.replicate_api_key
#API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V1.4"
#headers = {"Authorization": f"Bearer {config.huggingface_api_key}"}
#os.makedirs('chatbot_responses', exist_ok=True)
#os.makedirs('bookmarks', exist_ok=True)
#os.makedirs('controlnet_responses', exist_ok=True)

app = QApplication([])
window = QWidget()
window.resize(1800, 1000)

layout = QGridLayout(window)

# Create group boxes
fashionCycle = FashionCycle()

# Add group boxes to the layout
layout.addWidget(fashionCycle.chatBox, 0, 0, 8, 1)
layout.addWidget(fashionCycle.bookMark, 0, 1, 2, 3)
layout.addWidget(fashionCycle.controlNet, 0, 4, 8, 1)
layout.addWidget(fashionCycle.canvas, 2, 1, 6, 3)
layout.addWidget(fashionCycle.pallete, 7, 2, 1, 1)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())