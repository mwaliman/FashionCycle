from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLCDNumber, QLineEdit, QGridLayout, QWidget, QAbstractButton, QPushButton, QLabel, QListView, QComboBox, QTextEdit, QSlider , QGroupBox
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QImage, QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt, QPoint, QRect, QAbstractListModel, QModelIndex, QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from pallete import Pallete
from control_net import ControlNet
from chat_box import ChatBox
from bookmark import Bookmark
from canvas import Canvas
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

class FashionCycle:
    def __init__(self):
        self.chatBox = ChatBox()
        self.chatBox.setMaximumWidth(300)
        self.bookMark = Bookmark()
        self.pallete = Pallete()
        self.pallete.setMaximumWidth(350)
        self.controlNet = ControlNet()
        self.controlNet.setMaximumWidth(300)
        self.canvas = Canvas()