from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QPushButton, QWidget, QListWidget
from PyQt5.QtCore import Qt

from widgets import Partition, ImageWidget, TextWidget


class Browser(QListWidget):
    def __init__(self, player, color, screen_scale):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSpacing(0)

        self.setStyleSheet("""
            QListWidget {border: none; color: #ffffff; background-color: #222222;}
            QListWidget::item {padding-top: 5px; padding-bottom: 5px;}
            QListWidget::item:selected {background-color: #1a1a1a; color: white; outline: none; border: none; color: #ff5555;}
            QListWidget::item:hover {background-color: #2a2a2a; outline: none; color: #ff5555;}
            QListView { outline: 0;}
            QScrollBar:vertical {border: 1px solid #222222; background: #292929; width: 15px; margin: 0px 0px 0px 0px;}
            QScrollBar::handle:vertical {background: #191919; min-height: 20px; border-radius: 7px;}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {background: none; height: 0px;}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: #222222;}
            """)

        self.browser_font = QFont("Bahnschrift Semibold", int(18 / screen_scale))
        self.setFont(self.browser_font)

        self.itemClicked.connect(lambda item: player.filter_media(item.text(), 'director'))


class BrowserPanel(Partition):
    def __init__(self, player, color, screen_scale):
        super().__init__(color)
        self.setContentsMargins(16, 16, 16, 16)

        self.list_widget = Browser(player, color, screen_scale)

        # unique_items = {'All'} | {actor for med in player.media for actor in med.cast}
        unique_items = {'All'} | {f'{item.director} ({len([m for m in player.media if item.director == m.director])})' for item in player.media}
        sorted_items = sorted(unique_items)

        for item in sorted_items:
            self.list_widget.addItem(item)

        self.layout.addWidget(self.list_widget)
