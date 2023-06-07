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

class Canvas(QGroupBox):
    def __init__(self):
        super().__init__("Canvas")
        # self.label5 = QLabel("Widget 5")
        # self.button5 = QPushButton("Button 5")

        # canvasLayout = QGridLayout(self)
        # canvasLayout.addWidget(self.label5)
        # canvasLayout.addWidget(self.button5)