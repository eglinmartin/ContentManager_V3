import math

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QSpacerItem, QGridLayout, \
    QLabel, QScrollArea
from PyQt5.QtCore import Qt, QSize, QTimer

from widgets import Partition, ImageWidget, TextWidget


class SelectorItem(QWidget):
    def __init__(self, player, med_item):
        super().__init__()
        self.setStyleSheet(f"background-color: #292929")

        # Create vertical box
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create image button
        self.image_button = QPushButton()
        self.image_button.setIcon(player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\{med_item.code}"))
        self.image_button.clicked.connect(lambda: player.select_media(med_item.code))
        self.image_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create title label
        self.title_label = QLabel(med_item.title)
        self.title_label.setStyleSheet(f"color: #ffffff; text-align: left top; padding: 2px;")
        self.title_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.title_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Set font, font size and wrapping
        self.text_font = QFont("Bahnschrift Semibold", 11)
        self.title_label.setFont(self.text_font)
        self.title_label.setWordWrap(True)

        # Add both widgets to vertical box
        layout.addWidget(self.image_button, alignment=Qt.AlignTop)
        layout.addWidget(self.title_label, alignment=Qt.AlignTop)

    def resizeEvent(self, event):
        self.image_button.setFixedHeight(int(self.image_button.width() * 0.562))
        self.title_label.setFixedWidth(int(self.image_button.width()))
        self.title_label.setFixedHeight(int(self.image_button.width()/4))
        self.setFixedHeight(int(self.image_button.width()/4) + int(self.image_button.height()))


class SelectorPanel(Partition):
    def __init__(self, player, color):
        super().__init__(color)
        self.player = player
        self.icon_cache = {}

        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setAlignment(Qt.AlignTop)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {border: 1px solid #292929; background: #292929; width: 15px; margin: 0px 0px 0px 0px;}
            QScrollBar::handle:vertical {background: #191919; min-height: 20px; border-radius: 7px;}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {background: none; height: 0px;}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: #292929;}
        """)

        # Create outer container to allow widgets to top-align
        outer_container = QWidget()
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.setAlignment(Qt.AlignTop)
        outer_container.setLayout(outer_layout)

        # Create inner container for grid layout
        content_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        content_widget.setLayout(self.grid_layout)

        # Add content to outer container, and set container as scroll widget
        outer_layout.addWidget(content_widget)
        self.scroll_area.setWidget(outer_container)

        # For each media item, create a selector item element and add
        self.selector_buttons = []
        self.populate_selector()

        self.layout.addWidget(self.scroll_area)

    def populate_selector(self):
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.selector_buttons = []
        for i, med_item in enumerate(self.player.filtered_media):
            button = SelectorItem(self.player, med_item)
            self.selector_buttons.append(button)
            self.grid_layout.addWidget(button, i // 3, i % 3)

        self.scroll_area.widget().updateGeometry()
        self.updateGeometry()

        self.adjust_buttons_sizes()

    def adjust_buttons_sizes(self):
        for button in self.selector_buttons:
            w = int(self.width() / 3) - 40
            button.setMaximumWidth(w)
            button.setMaximumHeight(int(w * 0.562))
            button.image_button.setIconSize(QSize(w, int(w * 0.562)))
            button.title_label.setFixedWidth(button.image_button.width())

    def resizeEvent(self, event):
        for button in self.selector_buttons:
            # Set resizing on window change
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMaximumWidth(int(self.width() / 3) - 40)
            button.setMaximumHeight(int(button.width()* 0.562))
            button.image_button.setIconSize(QSize(button.width(), int(button.width()* 0.562)))
            button.title_label.setFixedWidth(button.image_button.width())
