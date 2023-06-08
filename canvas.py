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
    def __init__(self,bookmarks):
        super().__init__("Canvas")
        # self.label5 = QLabel("Widget 5")
        self.bookmarks = bookmarks
        self.setFixedSize(QSize(600,600))
        self.canvas = QImage(600,600, QImage.Format_RGB32)
        print('self',self.size())
        print('canvas',self.canvas.size())

        self.setMouseTracking(True)
        self.canvas = QImage(self.size(), QImage.Format_RGB32)
        self.canvas.fill(Qt.white)
        self.pen_thickness = 2
        self.eraseMode = False
        self.image_path = None
        self.bookmarks = bookmarks
        self.pallete = Pallete(self)

    def load_image(self, fname):
        self.image_path = './sketches/' + fname
        image = QImage(self.image_path)
        scaled_image = image.scaled(self.canvas.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.canvas = scaled_image.copy()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.canvas)

    def resizeEvent(self, event):
        new_size = event.size()
        new_canvas = QImage(new_size, QImage.Format_RGB32)
        new_canvas.fill(Qt.white)
        painter = QPainter(new_canvas)
        painter.drawImage(QPoint(0, 0), self.canvas)
        self.canvas = new_canvas

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            painter = QPainter(self.canvas)
            pen = QPen(QColor("black" if not self.eraseMode else "white"), self.pen_thickness, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_pos, event.pos())
            self.last_pos = event.pos()
            self.update()

    def set_pen_thickness(self, thickness):
        self.pen_thickness = thickness

    def set_eraser_mode(self):
        self.eraseMode = not self.eraseMode

    def add_image(self, image_path):
        self.image_path = image_path
        self.update()

    def save_image(self, filename):
        if self.image_path:
            self.canvas.save(self.image_path)
        else:
            sketches = [f for f in os.listdir('./sketches') if 'sketch' in f]
            self.canvas.save('./sketches/sketch' + str(len(sketches)) + '.jpg')

class Pallete(QGroupBox):
    def __init__(self,canvas):
        super().__init__("pallete")
        self.canvas = canvas
        self.ThicknessLabel = QLabel("Thickness")
        self.OpaquenessLabel = QLabel("Opaqueness")
        self.Erasing = QPushButton("Erase Mode")
        self.bookMarkSendFromCanvas = QPushButton("Save")
        self.bookMarkSendFromCanvas.clicked.connect(self.canvas.save_image)
        self.PixelThicknessSliderForPallete = QSlider()
        self.PixelOpaquenessSliderForPallete = QSlider()
        self.PixelThicknessSliderForPallete.setOrientation(Qt.Horizontal)  # Set the slider orientation to horizontal
        self.PixelThicknessSliderForPallete.setFixedSize(100, 20)
        self.PixelOpaquenessSliderForPallete.setOrientation(Qt.Horizontal)  # Set the slider orientation to horizontal
        self.PixelOpaquenessSliderForPallete.setFixedSize(100, 20)
        # self.PixelThicknessValueForPallete = QLCDNumber()
        # self.PixelThicknessValueForPallete.setFixedSize(50, 20)
        # self.PixelOpaquenessValueForPallete = QLCDNumber()
        # self.PixelOpaquenessValueForPallete.setFixedSize(50, 20)
        
        
        self.Erasing.raise_()
        self.bookMarkSendFromCanvas.raise_()
        self.PixelThicknessSliderForPallete.raise_()
        self.PixelOpaquenessSliderForPallete.raise_()
        
        self.Erasing.clicked.connect(self.eraserMode_change_text)
        self.Erasing.clicked.connect(self.canvas.set_eraser_mode)

        palleteLayout = QGridLayout(self)
        palleteLayout.addWidget(self.Erasing, 0, 0)
        palleteLayout.addWidget(self.bookMarkSendFromCanvas, 1, 0)
        palleteLayout.addWidget(self.PixelThicknessSliderForPallete, 0, 1)
        palleteLayout.addWidget(self.PixelOpaquenessSliderForPallete, 1, 1)
        palleteLayout.addWidget(self.ThicknessLabel, 0, 2)
        palleteLayout.addWidget(self.OpaquenessLabel, 1, 2)
        # palleteLayout.addWidget(self.PixelThicknessValueForPallete, 0, 3)
        # palleteLayout.addWidget(self.PixelOpaquenessValueForPallete, 1, 3)
        
        
        # self.PixelThicknessSliderForPallete.sliderMoved['int'].connect(self.PixelThicknessValueForPallete.display)
        # self.PixelOpaquenessSliderForPallete.sliderMoved['int'].connect(self.PixelOpaquenessValueForPallete.display)
    def eraserMode_change_text(self):
        global erase
        if erase == "yes":
            self.Erasing.setText("Eraser Mode: on")
            erase = "no"
        else:
            self.Erasing.setText("Eraser Mode: off")
            erase = "yes"
