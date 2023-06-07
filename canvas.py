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
        self.canvas = QImage(self.size(), QImage.Format_RGB32)

    #     self.canvas.fill(Qt.white)
    #     self.canvas.load('./sketches/black and white striped pants.jpg')
    #     self.currentColor = Qt.black
    #     self.currentSize = 2
    #     self.lastMousePos = QPoint()
        
    #     #This is for keeping track of how many times the mouse clicks happen in the app
    #     self.mousePressCount = 0
        
    #     #This keeps the user from drawing until the left mouse button is clicked
    #     self.draw = False


    # def size_2(self):
    #     self.currentSize = 2

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.draw = True
    #         self.lastMousePos = event.pos()
        
    #     self.coordFile = open("Mouse Coordinates.txt" , "a")
    #     self.mousePressCount = self.mousePressCount + 1
        
    #     if(self.mousePressCount > 1):
    #         self.coordFile.write("\n\nMouse Coordinate Set: " + str(self.mousePressCount))
            
    #     else:
    #         self.coordFile.write("Mouse Coordinate Set: " + str(self.mousePressCount))

    # #This will detect if the mouse is moving
    # def mouseMoveEvent(self, event):
    #     if(event.buttons() & Qt.LeftButton) & self.draw:
    #         painter = QPainter(self.canvas)
    #         painter.setPen(QPen(self.currentColor, self.currentSize))
    #         painter.drawLine(self.lastMousePos, event.pos())
    #         self.lastMousePos = event.pos()
    #         self.update()
    #         print((event.x(), event.y()))
    #         self.coordFile = open("Mouse Coordinates.txt", "a")
    #         self.coordFile.write("\nMouse Coordinates: (x:%d , y:%d)" % (event.x(), event.y()))

    # #This will detect if the mouse button has been released
    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.draw = False
    #         self.coordFile.close()

    # #This will allow painting to happen on the canvas
    # def paintEvent(self, event):
    #     canvasPainter  = QPainter(self)
    #     canvasPainter.begin(self)
    #     canvasPainter.drawImage(self.rect(),self.canvas)
    #     canvasPainter.end()

    # def saveImage(self):

    #     self.canvas.save('./canvas.jpg')

        self.setMouseTracking(True)
        self.canvas = QImage(self.size(), QImage.Format_RGB32)
        self.canvas.fill(Qt.white)
        self.pen_thickness = 2
        self.eraseMode = False
        self.image_path = None
        self.bookmarks = bookmarks

        image_path = './sketches/black and white striped pants.jpg'
        image = QImage(image_path)
        scaled_image = image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.canvas = scaled_image.copy()

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
        self.canvas.save(filename)



