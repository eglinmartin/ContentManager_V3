from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt

from widgets import Partition, ImageWidget, TextWidget


class PreviewPanel(Partition):
    def __init__(self, color):
        super().__init__(color)
