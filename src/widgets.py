from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QTextEdit, QLineEdit
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont, QPainter, QTextOption
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt

import handler


class ImageWidget(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent, back_col: str, font_col: str, alignment, text=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {back_col}; color: {font_col};")
        self.setAlignment(alignment)
        self.setWordWrap(True)
        self.pixmap_original = None  # Original pixmap loaded from the image
        self.pixmap_scaled = None  # Scaled pixmap for display
        self.text = text  # Text to display over image
        self.setMinimumSize(1, 1)  # Minimum size for the label

    def set_image(self, image_name: str):
        """
        Set image to new pixmap object
        """
        pixmap = QPixmap(image_name)

        if pixmap.isNull():
            print(f"Failed to load image: {image_name}")
            return

        self.pixmap_original = pixmap
        self.update_image()

    def resizeEvent(self, event):
        """
        On resize, scale the image with the window, keeping it as a square
        """
        super().resizeEvent(event)
        side_length = self.width()
        self.resize(side_length, side_length)
        self.update_image()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def update_image(self):
        """
        Update the image, re-transforming it to new window scale
        """
        if self.pixmap_original:
            # Scale the pixmap to the label's width and height dynamically
            self.pixmap_scaled = self.pixmap_original.scaled(
                self.width(), self.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(self.pixmap_scaled)


class TextWidget(QTextEdit):
    def __init__(self, parent=None, font_col="#ffffff", font=None, alignment=Qt.AlignLeft, back_colour="transparent", column=None):
        super().__init__(parent)

        if font:
            self.setFont(font)

        self.setStyleSheet(
            f"""color: {font_col}; background-color: {back_colour}; border: none;"""
        )

        self.setAlignment(alignment)

        # Enable word wrap
        self.setWordWrapMode(QTextOption.WordWrap)

        # No scrollbars
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Expand horizontally, but the HEIGHT will be controlled manually
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Connect text changes → resize
        self.textChanged.connect(self.updateHeight)
        self.updateHeight()  # set initial height

        self.parent = parent
        self.column = column

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            handler.update_db(player=self.parent.player, column=self.column, value=self.toPlainText())
            event.accept()
        else:
            super().keyPressEvent(event)

    def updateHeight(self):
        doc = self.document()
        doc.setTextWidth(self.viewport().width())
        newHeight = doc.size().height() + 6   # padding

        self.setFixedHeight(int(newHeight))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # recalc height when width changes
        self.updateHeight()

    def set_text(self, text):
        self.setPlainText(text)
        self.updateHeight()


class Partition(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.setLayout(self.layout)


    def add_widget(self, widget):
        self.layout.addWidget(widget)

