from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QAbstractButton, QPushButton, QLabel, QListView, QComboBox, QTextEdit
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

class CanvasWidget(QWidget):
    def __init__(self,bookmarks):
        super().__init__()
        self.setMouseTracking(True)
        self.paths = []
        self.current_path = QPainterPath()
        self.pen_thickness = 2
        self.eraseMode = False
        self.image_path = None
        self.bookmarks = bookmarks

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
        if self.eraseMode:
            pen = QPen(Qt.white, self.pen_thickness)
            painter.setPen(pen)
            painter.drawPath(self.current_path)
        else:
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