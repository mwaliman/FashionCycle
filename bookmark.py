from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QScrollBar, QListView, QAbstractItemView, QListWidgetItem, QMainWindow, QVBoxLayout, QLCDNumber, QLineEdit, QGridLayout, QWidget, QAbstractButton, QPushButton, QLabel, QListWidget,QHBoxLayout, QComboBox, QTextEdit, QSlider , QGroupBox
from PyQt5.QtGui import QPainter, QColor, QStandardItemModel, QStandardItem, QPen, QPainterPath, QImage, QPixmap, QIcon
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
#from CanvasWidget import CanvasWidget

class Bookmark(QGroupBox):
    def __init__(self):
        super().__init__("bookMark")
        self.bookMarkDisplayOnCanvasButton = QPushButton("Display")
        self.bookMarkLIstOfImages = QComboBox()
        self.bookMarkDisplayOnCanvasButton.setFixedSize(100, 30)

        bookMarkLayout = QGridLayout(self)
        bookMarkLayout.addWidget(self.bookMarkLIstOfImages, 0, 0)
        bookMarkLayout.addWidget(self.bookMarkDisplayOnCanvasButton, 0, 1)

        self.bookMarkDisplayOnCanvasButton.clicked.connect(self.add_group_box)
        
        # Create a QListView with horizontal scrolling
        list_view = QListView()
        list_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        list_view.setFlow(QListView.LeftToRight)
        list_view.setResizeMode(QListView.Adjust)
        list_view.setWrapping(False)
        list_view.setSpacing(10)
        list_view.setSelectionMode(QAbstractItemView.NoSelection)

        # Set a custom QScrollBar for horizontal scrolling
        scroll_bar = QScrollBar(Qt.Horizontal)
        list_view.setHorizontalScrollBar(scroll_bar)

        # Create a QStandardItemModel for the list view
        self.model = QStandardItemModel()
        list_view.setModel(self.model)

        bookMarkLayout.addWidget(list_view)

    def add_group_box(self):
        # Create a new QGroupBox
        group_box = QGroupBox(self)
        group_box.setTitle("Group Box")

        # Create a QHBoxLayout for the group box
        layout = QHBoxLayout(group_box)
        group_box.setLayout(layout)

        # Load and display the image
        self.load_image(group_box, "./bookmarks/red dress.jpg", desired_width=100, desired_height=100)

        # Create a QPushButton for remove
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_group_box(group_box))
        layout.addWidget(remove_button)

        # Add the QGroupBox to the QStandardItemModel
        item = QStandardItem()
        item.setSizeHint(group_box.sizeHint())
        self.model.appendRow(item)
        self.model.setItem(item.row(), item.column(), item)
        index = self.model.indexFromItem(item)

        # Add the QGroupBox to the QListView
        list_view = self.findChild(QListView)
        list_view.setIndexWidget(index, group_box)

    def remove_group_box(self, group_box):
        list_view = self.findChild(QListView)
        index = self.model.indexFromItem(self.model.item(0))
        while index.isValid():
            widget = list_view.indexWidget(index)
            if widget == group_box:
                self.model.removeRow(index.row())
                break
            index = self.model.index(index.row() + 1, index.column())

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
