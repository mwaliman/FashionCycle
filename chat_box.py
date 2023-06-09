from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QMainWindow, QListView, QVBoxLayout, QLCDNumber, QLineEdit, QGridLayout, QWidget, QAbstractButton, QPushButton, QLabel, QListWidget,QHBoxLayout, QComboBox, QTextEdit, QSlider , QGroupBox
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
import config
import replicate
import shutil

os.environ["REPLICATE_API_TOKEN"] = config.replicate_api_key
API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V1.4"
headers = {"Authorization": f"Bearer {config.huggingface_api_key}"}
os.makedirs('chatbot_responses', exist_ok=True)
os.makedirs('bookmarks', exist_ok=True)
os.makedirs('controlnet_responses', exist_ok=True)

class ChatBox(QGroupBox):
    def __init__(self, bookmarks):
        super().__init__("Inspiration")
        self.chatMessageSend = QPushButton("Generate")
        self.chatMessage = QLineEdit("")
        self.chatMessage.setPlaceholderText("Describe here...")
        self.bookmarks = bookmarks
        self.recentReponseImageDisplay = QLabel("")
        self.recentReponseImageDisplay.setFixedSize(280, 280)
        self.recentReponseImageDisplay.setStyleSheet("QLabel { background-color: white; border: 1px solid #444444; }")

        
        # recentReponseImageDisplayLayout = QHBoxLayout(self.recentReponseImageDisplay)
        # self.recentReponseImageDisplay.setLayout(recentReponseImageDisplayLayout)
        
        chatBoxLayout = QGridLayout(self)
        chatBoxLayout.addWidget(self.chatMessage, 1, 0, 1, 3)
        chatBoxLayout.addWidget(self.chatMessageSend, 1, 3)
        chatBoxLayout.addWidget(self.recentReponseImageDisplay, 0, 0, 1, 4)
        
        self.chatMessageSend.clicked.connect(self.add_group_box)
        
        list_widget = QListWidget()
        chatBoxLayout.addWidget(list_widget, 2, 0, 1, 4)

        self.list_widget = list_widget
        self.list_widget.setMinimumWidth(280)
        
        
    def generate_chatbot_response(self, message):
        clothing_description = message
        data = self.query("a full body, uncropped, head to toe photo of a single model wearing a "+ clothing_description + ", facing the camera, simple background")
        stream = io.BytesIO(data.content)
        img = Image.open(stream)
        img.save('./chatbot_responses/' + message + ".jpg")
        return './chatbot_responses/' + message + ".jpg"
        
    def query(self,payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return response
        
    def add_group_box(self):
        message = self.chatMessage.text()
        if message == "":
            return
        self.chatMessage.clear()
        response = self.generate_chatbot_response(message)
        #self.load_image(self.recentReponseImageDisplay, response, desired_width=280, desired_height=280)
        
        image = QImage(280,280, QImage.Format_RGB32)
        image.load(response)
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(280, 280, Qt.AspectRatioMode.KeepAspectRatio)
        self.recentReponseImageDisplay.setPixmap(pixmap)
        
        # Create a new QGroupBox
        group_box = QGroupBox(self)
        group_box.setTitle(message)

        # Create a QHBoxLayout for the group box
        layout = QHBoxLayout(group_box)
        group_box.setLayout(layout)

        # Load and display the image
        self.load_image(group_box, response, desired_width=100, desired_height=100)

        # Create a QPushButton
        bookMarkSend = QPushButton("Save")
        bookMarkSend.setFixedSize(100, 30)
        layout.addWidget(bookMarkSend)

        # Connect the button's clicked signal to the slot function
        bookMarkSend.clicked.connect(self.bookmark_clicked(message))
        
        # Create a QListWidgetItem and set the QGroupBox as its widget
        item = QListWidgetItem(self.list_widget)
        item.setSizeHint(group_box.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, group_box)

    def load_image(self, group_box, image_path, desired_width, desired_height):
        # Create a QLabel widget
        label = QLabel(group_box)

        # Create a QPixmap object with the image
        pixmap = QPixmap(image_path)

        # Scale the image while preserving aspect ratio
        pixmap = pixmap.scaled(desired_width, desired_height, Qt.AspectRatioMode.KeepAspectRatio)

        # Set the image to the QLabel
        label.setPixmap(pixmap)

        # Add the QLabel to the QHBoxLayout
        layout = group_box.layout()
        layout.addWidget(label)

    def bookmark_clicked(self, fname):

        def add_to_bookmarks():
            # add to folder bookmarks
            shutil.copyfile('./chatbot_responses/' + fname + ".jpg", './bookmarks/' + fname + ".jpg")
            self.bookmarks.add_group_box(fname)
        return add_to_bookmarks