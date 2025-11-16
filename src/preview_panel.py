from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt

from widgets import Partition, ImageWidget, TextWidget


class PlayerButton(QPushButton):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setStyleSheet(f'color: #ffffff;')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class PreviewPanel(Partition):
    def __init__(self, player, color, selected_media):
        super().__init__(color)

        # Create main image label
        self.label_image = ImageWidget(self, back_col='#694343', font_col='#ffffff', alignment=Qt.AlignCenter)
        self.label_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.label_image, alignment=Qt.AlignTop)

        # Create title label
        self.title_font = QFont("Bahnschrift Semibold", 18)
        self.label_title = TextWidget(self, font_col='#ffffff', font=self.title_font, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.label_title, alignment=Qt.AlignTop)

        # Create director label
        self.director_font = QFont("Bahnschrift Semibold", 16)
        self.label_director = TextWidget(self, font_col='#dddddd', font=self.director_font, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.label_director, alignment=Qt.AlignTop)

        # Create cast label
        self.cast_font = QFont("Bahnschrift Semibold", 12)
        self.label_cast = TextWidget(self, font_col='#dddddd', font=self.cast_font, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.label_cast, alignment=Qt.AlignTop)

        # Create blank space below media metadata
        self.layout.addStretch()

        # Create a horizontal layout for buttons
        self.player_menu = QWidget(self)
        self.player_menu.setStyleSheet(f"background-color : #1c1c1c")
        self.player_menu.setMinimumSize(1, 100)
        button_layout = QHBoxLayout(self.player_menu)

        button_shuffle = PlayerButton("Shuffle")
        button_shuffle.clicked.connect(player.shuffle)
        button_layout.addWidget(button_shuffle)

        button_previous = PlayerButton("Previous")
        button_previous.clicked.connect(player.select_previous)
        button_layout.addWidget(button_previous)

        button_play = PlayerButton("Play")
        button_layout.addWidget(button_play)

        button_next = PlayerButton("Next")
        button_next.clicked.connect(player.select_next)
        button_layout.addWidget(button_next)

        button_favourite = PlayerButton("Favourite")
        button_layout.addWidget(button_favourite)

        # Add the QWidget with the buttons to the main layout
        self.layout.addWidget(self.player_menu)

        self.update_panel(selected_media)

    def update_panel(self, selected_media):
        self.label_title.set_text(selected_media.title)
        self.label_director.set_text(selected_media.director)
        self.label_cast.set_text(', '.join(selected_media.cast))
        self.label_image.set_image(fr"C:\Storage\Programming\ContentManager_V3\bin\{selected_media.code}")
