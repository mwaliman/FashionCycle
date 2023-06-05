# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\FashionCycle.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath
from PyQt5.QtCore import Qt, QPoint, QRect
import requests
import json
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image
from io import BytesIO
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, QByteArray
import json
import requests
import io
from PIL import Image
from PyQt5.QtWidgets import QApplication, QListView, QWidget, QVBoxLayout
from PyQt5.QtCore import QAbstractListModel, Qt, QModelIndex
from PyQt5.QtGui import QPixmap
API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V1.4"
api_key = "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"
headers = {"Authorization": f"Bearer {api_key}"}


erase = "no"
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 1000)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        color = QColor(255, 255, 255)
        self.centralwidget.setStyleSheet("background-color: {}".format(color.name()))
        
        
        # Create a vertical layout for the central widget
        self.layout = QVBoxLayout(self.centralwidget)

        # Create a canvas widget for drawing
        self.canvas = CanvasWidget()
        self.layout.addWidget(self.canvas)

        # Set the main layout
        self.centralwidget.setLayout(self.layout)
        
        #the button that sends the image from bookmark to canvas
        self.bookMarkSendFromCanvas = QtWidgets.QPushButton(self.centralwidget)
        color = QColor(255, 255, 255)
        self.bookMarkSendFromCanvas.setStyleSheet("background-color: {}".format(color.name()))
        self.bookMarkSendFromCanvas.setGeometry(QtCore.QRect(1310, 910, 101, 28))
        self.bookMarkSendFromCanvas.setStyleSheet("")
        self.bookMarkSendFromCanvas.setObjectName("bookMarkSendFromCanvas")
        
        #the display that showed the pixel thickness of the brush
        self.PixelThicknessValueForPallete = QtWidgets.QLCDNumber(self.centralwidget)
        self.PixelThicknessValueForPallete.display(1)
        color = QColor(255, 255, 255)
        self.PixelThicknessValueForPallete.setStyleSheet("background-color: {}".format(color.name()))
        self.PixelThicknessValueForPallete.setGeometry(QtCore.QRect(810, 890, 111, 61))
        self.PixelThicknessValueForPallete.setStyleSheet("border: 1px solid black;")
        self.PixelThicknessValueForPallete.setObjectName("PixelThicknessValueForPallete")
        
        #the pop up tab that holds anything related to the chat box AI of stable diffusion
        self.chatBox = QtWidgets.QGroupBox(self.centralwidget)
        self.chatBox.setGeometry(QtCore.QRect(10, 10, 401, 951))
        color = QColor(102, 255, 255)
        self.chatBox.setStyleSheet("border: 1px solid black;""background-color: {}".format(color.name()))
        self.chatBox.setTitle("")
        self.chatBox.setFlat(True)
        self.chatBox.setObjectName("chatBox")
        
        #the chat Message History holds all the text that shows all the image and the User's input
        self.chatMessageHistory = QtWidgets.QTextBrowser(self.chatBox)
        self.chatMessageHistory.setGeometry(QtCore.QRect(10, 30, 371, 450))
        self.chatMessageHistory.setMinimumSize(QtCore.QSize(311, 450))
        self.chatMessageHistory.setAutoFillBackground(False)
        color = QColor(255, 255, 255)
        self.chatMessageHistory.setStyleSheet("background-color: {}".format(color.name()))
        self.chatMessageHistory.setObjectName("chatMessageHistory")
        
        #the button that sends the specific image in displayed will be sent to the book mark tab
        self.bookMarkSend = QtWidgets.QPushButton(self.chatBox)
        color = QColor(255, 255, 255)
        self.bookMarkSend.setStyleSheet("background-color: {}".format(color.name()))
        self.bookMarkSend.setGeometry(QtCore.QRect(330, 910, 41, 28))
        self.bookMarkSend.setObjectName("bookMarkSend")
        
        #the textbox that holds the user input to be sent into the chat message history
        self.chatMessage = QtWidgets.QTextEdit(self.chatBox)
        color = QColor(255, 255, 255)
        self.chatMessage.setStyleSheet("background-color: {}".format(color.name()))
        self.chatMessage.setGeometry(QtCore.QRect(10, 910, 261, 31))
        self.chatMessage.setObjectName("chatMessage")
        
        #the button that sends the chat message to the chat message history
        self.chatMessageSend = QtWidgets.QPushButton(self.chatBox)
        color = QColor(255, 255, 255)
        self.chatMessageSend.setStyleSheet("background-color: {}".format(color.name()))
        self.chatMessageSend.setGeometry(QtCore.QRect(280, 910, 41, 28))
        self.chatMessageSend.setObjectName("chatMessageSend")
        
        #the button that closes the chat box tab
        self.closeChatboxButton = QtWidgets.QPushButton(self.chatBox)
        self.closeChatboxButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(255, 0, 0), stop:1 rgb(255, 0, 0));")
        self.closeChatboxButton.setGeometry(QtCore.QRect(0, 0, 93, 28))
        self.closeChatboxButton.setObjectName("closeChatboxButton")
        
        #the pop up tab that holds anything related to the book mark or favorite
        self.bookMark = QtWidgets.QGroupBox(self.centralwidget)
        self.bookMark.setGeometry(QtCore.QRect(410, 10, 1021, 211))
        self.bookMark.setLayoutDirection(QtCore.Qt.LeftToRight)
        color = QColor(255, 255, 150)
        self.bookMark.setStyleSheet("border: 1px solid black;""background-color: {}".format(color.name()))
        self.bookMark.setTitle("")
        self.bookMark.setFlat(True)
        self.bookMark.setObjectName("bookMark")
        
        #the tab list that would show the images in a list
        self.bookMarkLIstOfImages = QtWidgets.QComboBox(self.bookMark)
        color = QColor(255, 255, 255)
        self.bookMarkLIstOfImages.setStyleSheet("background-color: {}".format(color.name()))
        self.bookMarkLIstOfImages.setGeometry(QtCore.QRect(360, 80, 531, 31))
        self.bookMarkLIstOfImages.setObjectName("bookMarkLIstOfImages")
        self.bookMarkLIstOfImages.addItem("")
        self.bookMarkLIstOfImages.addItem("")
        self.bookMarkLIstOfImages.addItem("")
        
        #the button that would send the selected image from control net to book mark
        self.bookMarkDisplayOnCanvasButton = QtWidgets.QPushButton(self.bookMark)
        color = QColor(255, 255, 255)
        self.bookMarkDisplayOnCanvasButton.setStyleSheet("background-color: {}".format(color.name()))
        self.bookMarkDisplayOnCanvasButton.setGeometry(QtCore.QRect(950, 180, 51, 28))
        self.bookMarkDisplayOnCanvasButton.setObjectName("bookMarkDisplayOnCanvasButton")
        
        #the button that closes the book mark tab
        self.closeBookMarkButton = QtWidgets.QPushButton(self.bookMark)
        color = QColor(255, 0, 0)
        self.closeBookMarkButton.setStyleSheet("background-color: {}".format(color.name()))
        self.closeBookMarkButton.setGeometry(QtCore.QRect(10, 0, 93, 28))
        self.closeBookMarkButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(255, 0, 0), stop:1 rgb(255, 0, 0));")
        self.closeBookMarkButton.setObjectName("closeBookMarkButton")
        
        #the display for the recent inputed image
        self.bookMarkDisplayOnCanvas = QtWidgets.QListView(self.bookMark)
        color = QColor(255, 255, 255)
        self.bookMarkDisplayOnCanvas.setStyleSheet("background-color: {}".format(color.name()))
        self.bookMarkDisplayOnCanvas.setGeometry(QtCore.QRect(120, 30, 171, 161))
        self.bookMarkDisplayOnCanvas.setObjectName("bookMarkDisplayOnCanvas")
        
        #the pop up tab that holds anything related to the book mark or favorite
        self.controlNet = QtWidgets.QGroupBox(self.centralwidget)
        self.controlNet.setGeometry(QtCore.QRect(1430, 10, 371, 931))
        color = QColor(0, 255, 0)
        self.controlNet.setStyleSheet("border: 1px solid black;""background-color: {}".format(color.name()))
        self.controlNet.setTitle("")
        self.controlNet.setFlat(True)
        self.controlNet.setObjectName("controlNet")
        
        #the button that would send the selected image from book mark to control net
        self.bookMarkSendFromControlNet = QtWidgets.QPushButton(self.controlNet)
        color = QColor(255, 255, 255)
        self.bookMarkSendFromControlNet.setStyleSheet("background-color: {}".format(color.name()))
        self.bookMarkSendFromControlNet.setGeometry(QtCore.QRect(140, 880, 101, 28))
        self.bookMarkSendFromControlNet.setObjectName("bookMarkSendFromControlNet")
        
        #the text that would hold the information to be sent to control net
        self.controlNetPromptInput = QtWidgets.QTextEdit(self.controlNet)
        color = QColor(255, 255, 255)
        self.controlNetPromptInput.setStyleSheet("background-color: {}".format(color.name()))
        self.controlNetPromptInput.setGeometry(QtCore.QRect(30, 120, 211, 31))
        self.controlNetPromptInput.setObjectName("controlNetPromptInput")
        
        #the slider that can be moved from 0 to 99 for the amount of control to control net
        self.controlNetSlider = QtWidgets.QSlider(self.controlNet)
        self.controlNetSlider.setGeometry(QtCore.QRect(120, 80, 160, 22))
        color = QColor(255, 255, 255)
        self.controlNetSlider.setStyleSheet("background-color: {}".format(color.name()))
        self.controlNetSlider.setOrientation(QtCore.Qt.Horizontal)
        self.controlNetSlider.setObjectName("controlNetSlider")
        
        #the value that is shown for the user to know how much control in control net
        self.controlNetValue = QtWidgets.QLCDNumber(self.controlNet)
        color = QColor(255, 255, 255)
        self.controlNetValue.setStyleSheet("background-color: {}".format(color.name()))
        self.controlNetValue.setGeometry(QtCore.QRect(120, 30, 161, 41))
        self.controlNetValue.setObjectName("controlNetValue")
        
        #the list that holds all the images from the output of control net
        self.controlNetImageList = QtWidgets.QListView(self.controlNet)
        color = QColor(255, 255, 255)
        self.controlNetImageList.setStyleSheet("background-color: {}".format(color.name()))
        self.controlNetImageList.setGeometry(QtCore.QRect(30, 400, 311, 440))
        self.controlNetImageList.setObjectName("controlNetImageList")
        
        #the button that would sent the prompt and the control value to the control net API
        self.controlNetSendPrompt = QtWidgets.QPushButton(self.controlNet)
        color = QColor(255, 255, 255)
        self.controlNetSendPrompt.setStyleSheet("background-color: {}".format(color.name()))
        self.controlNetSendPrompt.setGeometry(QtCore.QRect(250, 120, 101, 28))
        self.controlNetSendPrompt.setStyleSheet("")
        self.controlNetSendPrompt.setObjectName("controlNetSendPrompt")
        
        #the list that would show which choice for the control net to recieve from the book mark
        self.bookMarkSelectionToSendControlNet = QtWidgets.QComboBox(self.controlNet)
        color = QColor(255, 255, 255)
        self.bookMarkSelectionToSendControlNet.setStyleSheet("background-color: {}".format(color.name()))
        self.bookMarkSelectionToSendControlNet.setGeometry(QtCore.QRect(30, 160, 211, 31))
        self.bookMarkSelectionToSendControlNet.setObjectName("bookMarkSelectionToSendControlNet")
        self.bookMarkSelectionToSendControlNet.addItem("")
        self.bookMarkSelectionToSendControlNet.addItem("")
        self.bookMarkSelectionToSendControlNet.addItem("")
        
        #the list that would show which choice for the book mark to recieve from control net
        self.controlNetSelectionToSendBookMark = QtWidgets.QComboBox(self.controlNet)
        color = QColor(255, 255, 255)
        self.controlNetSelectionToSendBookMark.setStyleSheet("background-color: {}".format(color.name()))
        self.controlNetSelectionToSendBookMark.setGeometry(QtCore.QRect(30, 850, 311, 22))
        self.controlNetSelectionToSendBookMark.setObjectName("controlNetSelectionToSendBookMark")
        self.controlNetSelectionToSendBookMark.addItem("")
        self.controlNetSelectionToSendBookMark.addItem("")
        self.controlNetSelectionToSendBookMark.addItem("")
        self.controlNetSelectionToSendBookMark.addItem("")
        
        #the button that close the control net tab
        self.closeControlNetButton = QtWidgets.QPushButton(self.controlNet)
        color = QColor(255, 0, 0)
        self.closeControlNetButton.setStyleSheet("background-color: {}".format(color.name()))
        self.closeControlNetButton.setGeometry(QtCore.QRect(10, 0, 93, 28))
        self.closeControlNetButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(255, 0, 0), stop:1 rgb(255, 0, 0));")
        self.closeControlNetButton.setObjectName("closeControlNetButton")
        
        #the image that is displayed in the controlNet display box
        self.controlNetImageDisplay = QtWidgets.QListView(self.controlNet)
        color = QColor(255, 255, 255)
        self.controlNetImageDisplay.setStyleSheet("background-color: {}".format(color.name()))
        self.controlNetImageDisplay.setGeometry(QtCore.QRect(100, 220, 171, 161))
        self.controlNetImageDisplay.setObjectName("controlNetImageDisplay")
        
        #the button that would open the chat box tab
        self.ChatbotTab = QtWidgets.QPushButton(self.centralwidget)
        color = QColor(255, 255, 255)
        self.ChatbotTab.setStyleSheet("background-color: {}".format(color.name()))
        self.ChatbotTab.setGeometry(QtCore.QRect(0, 460, 93, 28))
        self.ChatbotTab.setObjectName("ChatbotTab")
        self.ChatbotTab.setVisible(False)
        
        #the button that would open the book mark tab
        self.BookmarkTab = QtWidgets.QPushButton(self.centralwidget)
        color = QColor(255, 255, 255)
        self.BookmarkTab.setStyleSheet("background-color: {}".format(color.name()))
        self.BookmarkTab.setGeometry(QtCore.QRect(870, 20, 93, 28))
        self.BookmarkTab.setObjectName("BookmarkTab")
        self.BookmarkTab.setVisible(False)
        
        #the button that would open the control net tab
        self.ControlNet = QtWidgets.QPushButton(self.centralwidget)
        color = QColor(255, 255, 255)
        self.ControlNet.setStyleSheet("background-color: {}".format(color.name()))
        self.ControlNet.setGeometry(QtCore.QRect(1710, 460, 93, 28))
        self.ControlNet.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.ControlNet.setObjectName("ControlNet")
        self.ControlNet.setVisible(False)
        
        #the button that turns eraser mode on or off
        self.Erasing = QtWidgets.QPushButton(self.centralwidget)
        self.Erasing.setGeometry(QtCore.QRect(1210, 910, 101, 28))
        self.Erasing.setStyleSheet("")
        self.Erasing.setObjectName("Erasing")
        
        #the slider that changes the value of the pen thickness
        self.PixelThicknessSliderForPallete = QtWidgets.QSlider(self.centralwidget)
        self.PixelThicknessSliderForPallete.setRange(1,16)
        self.PixelThicknessSliderForPallete.setGeometry(QtCore.QRect(930, 910, 160, 22))
        self.PixelThicknessSliderForPallete.setOrientation(QtCore.Qt.Horizontal)
        self.PixelThicknessSliderForPallete.setObjectName("PixelThicknessSliderForPallete")
        
        #the display for the recent inputed image
        self.chatImageResponseDisplay = QtWidgets.QListView(self.chatBox)
        color = QColor(255, 255, 255)
        self.chatImageResponseDisplay.setStyleSheet("background-color: {}".format(color.name()))
        self.chatImageResponseDisplay.setGeometry(QtCore.QRect(10, 490, 371, 411))
        self.chatImageResponseDisplay.setObjectName("chatImageResponseDisplay")
        self.chatImageResponseDisplay.setViewMode(QListView.IconMode)
        self.chatImageResponseDisplay.setResizeMode(QListView.Adjust)
        
        self.bookMarkSend.raise_()
        
        self.chatMessage.raise_()
        
        self.chatMessageSend.raise_()
        
        self.closeChatboxButton.raise_()
        
        self.chatMessageHistory.raise_()
        
        self.BookmarkTab.raise_()
        
        self.ControlNet.raise_()
        
        self.ChatbotTab.raise_()
        
        self.bookMarkSendFromCanvas.raise_()
        
        self.PixelThicknessValueForPallete.raise_()
        
        self.bookMark.raise_()
        
        self.chatBox.raise_()
        
        self.controlNet.raise_()
        
        self.Erasing.raise_()
        
        self.PixelThicknessSliderForPallete.raise_()
        
        self.chatImageResponseDisplay.raise_()
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1800, 26))
        self.menubar.setObjectName("menubar")
        
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        
        MainWindow.setStatusBar(self.statusbar)

    #untouched generated code starts here
        self.retranslateUi(MainWindow)
        self.controlNetSlider.sliderMoved['int'].connect(self.controlNetValue.display) # type: ignore
        self.closeControlNetButton.clicked.connect(self.controlNet.close) # type: ignore
        self.closeBookMarkButton.clicked.connect(self.bookMark.close) # type: ignore
        self.closeChatboxButton.clicked.connect(self.chatBox.close) # type: ignore
        self.ControlNet.clicked.connect(self.controlNet.show) # type: ignore
        self.BookmarkTab.clicked.connect(self.bookMark.show) # type: ignore
        self.ChatbotTab.clicked.connect(self.chatBox.show) # type: ignore
        self.closeControlNetButton.clicked.connect(self.ControlNet.show) # type: ignore
        self.ControlNet.clicked.connect(self.ControlNet.hide) # type: ignore
        self.closeBookMarkButton.clicked.connect(self.BookmarkTab.show) # type: ignore
        self.BookmarkTab.clicked.connect(self.BookmarkTab.hide) # type: ignore
        self.ChatbotTab.clicked.connect(self.ChatbotTab.hide) # type: ignore
        self.closeChatboxButton.clicked.connect(self.ChatbotTab.show) # type: ignore
        self.PixelThicknessSliderForPallete.sliderMoved['int'].connect(self.PixelThicknessValueForPallete.display) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    #untouched generated code ends here
        self.chatMessageSend.clicked.connect(self.send_message_to_Chatbot)
        self.controlNetSendPrompt.clicked.connect(self.send_prompt_to_ControlNet)
        self.PixelThicknessSliderForPallete.valueChanged.connect(self.canvas.set_pen_thickness)
        self.Erasing.clicked.connect(self.eraserMode_change_text)
        self.Erasing.clicked.connect(self.canvas.set_eraser_mode)
        self.canvas.add_image("response2.png")
        image_paths = ['response2.png','cat.png']
        image_model = ImageListModel(image_paths)
        self.chatImageResponseDisplay.setModel(image_model)
        #untouched generated code starts here
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.bookMarkSendFromCanvas.setText(_translate("MainWindow", "Book Mark"))
        self.chatMessageHistory.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.bookMarkSend.setText(_translate("MainWindow", "BM"))
        self.chatMessageSend.setText(_translate("MainWindow", "Send"))
        self.closeChatboxButton.setText(_translate("MainWindow", "Close"))
        self.bookMarkLIstOfImages.setItemText(0, _translate("MainWindow", "Nice"))
        self.bookMarkLIstOfImages.setItemText(1, _translate("MainWindow", "NotNice"))
        self.bookMarkLIstOfImages.setItemText(2, _translate("MainWindow", "Comething"))
        self.bookMarkDisplayOnCanvasButton.setText(_translate("MainWindow", "Display"))
        self.closeBookMarkButton.setText(_translate("MainWindow", "Close"))
        self.bookMarkSendFromControlNet.setText(_translate("MainWindow", "Book Mark"))
        self.controlNetSendPrompt.setText(_translate("MainWindow", "Send"))
        self.bookMarkSelectionToSendControlNet.setItemText(0, _translate("MainWindow", "Nice"))
        self.bookMarkSelectionToSendControlNet.setItemText(1, _translate("MainWindow", "NotNice"))
        self.bookMarkSelectionToSendControlNet.setItemText(2, _translate("MainWindow", "Comething"))
        self.controlNetSelectionToSendBookMark.setItemText(0, _translate("MainWindow", "Choice 1"))
        self.controlNetSelectionToSendBookMark.setItemText(1, _translate("MainWindow", "Choice 2"))
        self.controlNetSelectionToSendBookMark.setItemText(2, _translate("MainWindow", "Choice 3"))
        self.controlNetSelectionToSendBookMark.setItemText(3, _translate("MainWindow", "Choice 4"))
        self.closeControlNetButton.setText(_translate("MainWindow", "Close"))
        self.ChatbotTab.setText(_translate("MainWindow", "Chatbot"))
        self.BookmarkTab.setText(_translate("MainWindow", "Book Mark"))
        self.ControlNet.setText(_translate("MainWindow", "ControlNet"))
        self.Erasing.setText(_translate("MainWindow", "Eraser Mode: off"))
    #untouched generated code ends here
    def eraserMode_change_text(self):
        global erase
        if erase == "yes":
            self.Erasing.setText("Eraser Mode: on")
            erase = "no"
        else:
            self.Erasing.setText("Eraser Mode: off")
            erase = "yes"
    def send_message_to_Chatbot(self):
        message = self.chatMessage.toPlainText()
        self.chatMessage.clear()
        self.chatMessageHistory.append(f"User: {message}")
        response = self.generate_chatbot_response(message)
        # print(response)
        # print(self.PixelThicknessSliderForPallete.sliderPosition())
        self.chatMessageHistory.append(f"ChatBot: {response}")
    def send_prompt_to_ControlNet(self):
        message = self.controlNetPromptInput.toPlainText()
        self.controlNetPromptInput.clear()
        value = str(self.controlNetValue.value())
        print(message + " " + value)
    def generate_chatbot_response(self, message):
        # floor length denim overalls
        clothing_description = message
        data = self.query("a full body, uncropped, head to toe photo of a single model wearing a "+ clothing_description + ", facing the camera, simple background")
        stream = io.BytesIO(data.content)
        img = Image.open(stream)
        img.save(message + ".png")
    def query(self,payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return response
    def add_item(self):
        item_text = self.input_text.text()
        if item_text:
            item = QStandardItem(item_text)
            self.model.appendRow(item)
            self.input_text.clear()

    def remove_item(self):
        selected_indexes = self.list_view.selectedIndexes()
        if selected_indexes:
            for index in selected_indexes:
                self.model.removeRow(index.row())
class ImageListModel(QAbstractListModel):
    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths

    def rowCount(self, parent=QModelIndex()):
        return len(self.image_paths)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.image_paths[index.row()]

        if role == Qt.DecorationRole:
            pixmap = QPixmap(self.image_paths[index.row()])
            return pixmap.scaledToHeight(100)

        return None
class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.paths = []
        self.current_path = QPainterPath()
        self.pen_thickness = 2
        self.eraseMode = False
        self.image_path = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.image_path:
            image = QImage(self.image_path)
            if not image.isNull():
                scaled_image = self.scale_image(image, self.width(), self.height())
                image_pos = self.calculate_image_position(scaled_image.width(), scaled_image.height())
                painter.drawImage(image_pos, scaled_image)

        for path, thickness, erase in self.paths:
            pen = QPen(Qt.white if erase else Qt.black, thickness)
            painter.setPen(pen)
            painter.drawPath(path)

        pen = QPen(Qt.black, self.pen_thickness)
        painter.setPen(pen)
        painter.drawPath(self.current_path)

    def scale_image(self, image, width, height):
        aspect_ratio = image.width() / image.height()
        target_aspect_ratio = width / height

        if aspect_ratio > target_aspect_ratio:
            target_width = width
            target_height = int(width / aspect_ratio)
        else:
            target_height = height
            target_width = int(height * aspect_ratio)

        scaled_image = image.scaled(target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio)
        return scaled_image

    def calculate_image_position(self, image_width, image_height):
        canvas_width = self.width()
        canvas_height = self.height()

        x = (canvas_width - image_width) // 2
        y = (canvas_height - image_height) // 2

        return QPoint(x, y)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.eraseMode:
                pen = QPen(Qt.NoPen)
            else:
                pen = QPen(Qt.black, self.pen_thickness)
            self.current_path = QPainterPath()
            self.current_path.moveTo(event.pos())
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.eraseMode:
                pen = QPen(Qt.NoPen)
            else:
                pen = QPen(Qt.black, self.pen_thickness)
            self.current_path.lineTo(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            erase = self.eraseMode
            self.paths.append((self.current_path, self.pen_thickness, erase))
            self.current_path = QPainterPath()
            self.update()

    def set_pen_thickness(self, thickness):
        self.pen_thickness = thickness
        self.update()
    
    def set_eraser_mode(self):
        self.eraseMode = not self.eraseMode
    
    def add_image(self, image_path):
        self.image_path = image_path
        self.update()

    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
