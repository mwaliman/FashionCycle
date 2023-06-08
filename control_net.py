from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QMainWindow, QVBoxLayout, QListView, QLCDNumber, QLineEdit, QGridLayout, QWidget, QAbstractButton, QPushButton, QLabel, QListWidget,QHBoxLayout, QComboBox, QTextEdit, QSlider , QGroupBox
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QImage, QPixmap, QIcon
from PyQt5.QtCore import QSize, pyqtSignal, Qt, QPoint, QRect, QAbstractListModel, QModelIndex, QUrl, QByteArray
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
class ControlNet(QGroupBox):
    def __init__(self, bookmarks):
        super().__init__("Prototype")
        _translate = QtCore.QCoreApplication.translate
        self.controlNetSendPrompt = QPushButton("Generate")
        self.controlNetSendPrompt.clicked.connect(self.add_group_box)
        self.controlNetPromptInput = QLineEdit("")
        self.controlNetPromptInput.setPlaceholderText("Describe here...")
        self.bookMarkSelectionToSendControlNet = QComboBox()
        self.bookMarkSelectionToSendControlNet.addItem("Select One")
        self.bookMarkSelectionToSendControlNet.setItemData(0, False)
        self.bookMarkSelectionToSendControlNet.setFixedSize(280, 30)
        self.controlNetSlider = QSlider()
        self.controlNetSlider.setOrientation(Qt.Horizontal)  # Set the slider orientation to horizontal
        self.controlNetSlider.setFixedSize(200, 20)
        self.controlNetValue = QLabel("Control:50%")
        self.controlNetValue.setFixedSize(80, 20)
        self.bookmarks = bookmarks
        self.recentReponseImageDisplay = QLabel("")
        self.recentReponseImageDisplay.setFixedSize(280, 280)
        self.recentReponseImageDisplay.setStyleSheet("QLabel { background-color: white; border: 1px solid #444444; }")

        controlNetLayout = QGridLayout(self)
        controlNetLayout.addWidget(self.controlNetPromptInput, 2, 0, 1, 3)
        controlNetLayout.addWidget(self.controlNetSendPrompt, 2, 3)
        controlNetLayout.addWidget(self.controlNetValue, 3, 0)
        controlNetLayout.addWidget(self.controlNetSlider, 3, 1, 1, 3)
        controlNetLayout.addWidget(self.bookMarkSelectionToSendControlNet, 1, 0, 1, 2)
        controlNetLayout.addWidget(self.recentReponseImageDisplay, 0, 0, 1, 2)
        
        for i, f in enumerate(os.listdir('bookmarks')):
            self.bookMarkSelectionToSendControlNet.addItem(f)

        self.controlNetSlider.setRange(0,100)
        self.controlNetSlider.setValue(50)
        self.controlNetSlider.valueChanged.connect(self.update_label)
        bookmarks.custom_signal.connect(self.handle_custom_signal)
        self.bookMarkSelectionToSendControlNet.currentIndexChanged.connect(self.selected)
        
        list_widget = QListWidget()
        controlNetLayout.addWidget(list_widget, 4, 0, 1, 1)

        self.list_widget = list_widget
        self.list_widget.setMinimumWidth(280)

    def control_Net(self, image_input, prompt_input, scale_input):
        output = replicate.run("jagilley/controlnet-canny:aff48af9c68d162388d230a2ab003f68d2638d88307bdaf1c2f1ac95079c9613",
        input={"image": open('./bookmarks/' + image_input, "rb"),
    		"prompt": prompt_input,
    		"scale":scale_input}
            )
        img_data = requests.get(output[-1]).content
        #print(image_input)

        # stick prompt in here somehow

        with open('./controlnet_responses/' + prompt_input + '.jpg', 'wb') as handler:
            handler.write(img_data)
        return prompt_input
        
    def handle_custom_signal(self, data):
        if data == "Deleted":
            print("it got through")
            self.bookMarkSelectionToSendControlNet.clear()
            self.bookMarkSelectionToSendControlNet.addItem("Select One")
            self.bookMarkSelectionToSendControlNet.setItemData(0, False)
            for i, f in enumerate(os.listdir('bookmarks')):
                self.bookMarkSelectionToSendControlNet.addItem(f)
        else:
            self.bookMarkSelectionToSendControlNet.addItem(data)
    def add_group_box(self):
        prompt = self.controlNetPromptInput.text()
        self.controlNetPromptInput.clear()
        img_fname = self.bookMarkSelectionToSendControlNet.currentText()
        if img_fname == "Select One":
            return
        else:
            value = 30*(self.controlNetSlider.value())/100
            response_fname = self.control_Net(img_fname,prompt,value)

            # Create a new QGroupBox
            group_box = QGroupBox(self)
            group_box.setTitle(prompt)

            # Create a QHBoxLayout for the group box
            layout = QHBoxLayout(group_box)
            group_box.setLayout(layout)

            # Load and display the image
            #print(response_fname)
            self.load_image(group_box, './controlnet_responses/' + response_fname + '.jpg', desired_width=100, desired_height=100)

            # Create a QPushButton
            bookMarkSelectionToSendControlNet = QPushButton("📌")
            bookMarkSelectionToSendControlNet.setFixedSize(100, 30)
            layout.addWidget(bookMarkSelectionToSendControlNet)

            # Connect the button's clicked signal to the slot function
            bookMarkSelectionToSendControlNet.clicked.connect(self.bookmark_clicked(response_fname))
        
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
            #print(fname)
            shutil.copyfile('./controlnet_responses/' + fname + ".jpg", './bookmarks/' + fname + ".jpg")
            self.bookmarks.add_group_box(fname)
        self.bookMarkSelectionToSendControlNet.addItem(fname + ".jpg")
        return add_to_bookmarks


    def selected(self):
        img_fname = self.bookMarkSelectionToSendControlNet.currentText()
        if img_fname == "Select One":
            return
        else:
            image_input = './bookmarks/' + img_fname
            image = QImage(280,280, QImage.Format_RGB32)
            image.load(image_input)
            pixmap = QPixmap.fromImage(image)
            pixmap = pixmap.scaled(280, 280, Qt.AspectRatioMode.KeepAspectRatio)
            self.recentReponseImageDisplay.setPixmap(pixmap)
    
    def update_label(self, value):
        self.controlNetValue.setText(f"Control:{value}%")
        