from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt


class ImageWidget(QLabel):
    def __init__(self, parent, back_col: str, font_col: str, alignment):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {back_col}; color: {font_col};")
        self.setAlignment(alignment)
        self.setWordWrap(True)
        self.pixmap_original = None
        self.setMinimumSize(1, 1)

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

    def update_image(self):
        """
        Update the image, re-transforming it to new window scale
        """
        if self.pixmap_original:
            # Scale the pixmap to the label's width and height dynamically
            scaled_pixmap = self.pixmap_original.scaled(
                self.width(), self.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled_pixmap)


class TextWidget(QLabel):
    def __init__(self, parent, font_col: str, font: QFont, alignment):
        super().__init__(parent)
        self.setFont(font)
        self.setStyleSheet(f"color: {font_col};")
        self.setAlignment(alignment)
        self.setWordWrap(True)
        self.setMinimumSize(1, 1)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def set_text(self, text):
        self.setText(text)


class Partition(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

    def add_widget(self, widget):
        self.layout.addWidget(widget)

