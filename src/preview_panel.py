from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt, QSize

from widgets import Partition, ImageWidget, TextWidget


class PlayerButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f'color: #ffffff;')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class PreviewPanel(Partition):
    def __init__(self, player, color, selected_media, screen_scale):
        super().__init__(color)
        self.layout.setSpacing(0)
        self.player = player

        # Create main image label
        self.label_image = ImageWidget(self, back_col='#252525', font_col='#ffffff', alignment=Qt.AlignCenter)
        self.label_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.label_image, alignment=Qt.AlignTop)

        self.layout.addSpacing(10)

        # Create title label
        self.title_font = QFont("Bahnschrift Semibold", int(32 / screen_scale))
        self.label_title = TextWidget(self, font_col='#ffffff', font=self.title_font, alignment=Qt.AlignLeft, back_colour='#252525', column='Title')
        self.layout.addWidget(self.label_title, alignment=Qt.AlignTop)

        # Create director label
        self.director_font = QFont("Bahnschrift Semibold", int(24 / screen_scale))
        self.label_director = TextWidget(self, font_col='#aaaaaa', font=self.director_font, alignment=Qt.AlignLeft, back_colour='#252525', column='Director')
        self.layout.addWidget(self.label_director, alignment=Qt.AlignTop)

        # Create cast label
        self.cast_font = QFont("Bahnschrift Semibold", int(20 / screen_scale))
        self.label_cast = TextWidget(self, font_col='#777777', font=self.cast_font, alignment=Qt.AlignLeft, back_colour='#252525', column='Cast')
        self.layout.addWidget(self.label_cast, alignment=Qt.AlignTop)

        # Create tags label
        self.tags_font = QFont("Bahnschrift Semibold", int(16 / screen_scale))
        self.label_tags = TextWidget(self, font_col='#666666', font=self.tags_font, alignment=Qt.AlignLeft, back_colour='#252525', column='Tags')
        self.layout.addWidget(self.label_tags, alignment=Qt.AlignTop)

        # Create blank space below media metadata
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addStretch()

        # Create a horizontal layout for buttons
        self.player_menu = QWidget(self)
        self.player_menu.setStyleSheet(f"background-color : #1c1c1c")
        self.player_menu.setMinimumSize(1, 100)

        self.button_layout = QHBoxLayout(self.player_menu)

        self.button_shuffle = PlayerButton()
        self.button_shuffle.setIcon(player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\icon_shuffle.png"))
        self.button_shuffle.clicked.connect(player.shuffle)
        self.button_layout.addWidget(self.button_shuffle)

        self.button_previous = PlayerButton()
        self.button_previous.setIcon(player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\icon_prev.png"))
        self.button_previous.clicked.connect(player.select_previous)
        self.button_layout.addWidget(self.button_previous)

        self.button_play = PlayerButton()
        self.button_play.setIcon(player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\icon_play.png"))
        self.button_layout.addWidget(self.button_play)

        self.button_next = PlayerButton()
        self.button_next.setIcon(player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\icon_next.png"))
        self.button_next.clicked.connect(player.select_next)
        self.button_layout.addWidget(self.button_next)

        self.button_favourite = PlayerButton()
        self.button_favourite.setIcon(player.get_icon(fr"C:\Storage\Programming\ContentManager_V3\bin\icon_fav.png"))
        self.button_layout.addWidget(self.button_favourite)

        self.layout.addWidget(self.player_menu)

        self.update_panel(selected_media)

    def resizeEvent(self, event):
        self.player_menu.adjustSize()
        self.label_image.setMaximumSize(self.label_image.width(), int(self.label_image.width()* 0.562))

        button_size = self.button_play.width()
        self.button_shuffle.setFixedHeight(button_size)
        self.button_previous.setFixedHeight(button_size)
        self.button_play.setFixedHeight(button_size)
        self.button_next.setFixedHeight(button_size)
        self.button_favourite.setFixedHeight(button_size)
        self.player_menu.setFixedHeight(button_size + 20)

        icon_size = QSize(int(button_size * 0.60), int(button_size * 0.60))
        self.button_shuffle.setIconSize(icon_size)
        self.button_previous.setIconSize(icon_size)
        self.button_play.setIconSize(icon_size)
        self.button_next.setIconSize(icon_size)
        self.button_favourite.setIconSize(icon_size)

    def update_panel(self, selected_media):
        self.label_title.set_text(selected_media.title)
        self.label_director.set_text(selected_media.director)
        self.label_cast.set_text(', '.join(selected_media.cast))

        if selected_media.tags:
            tags_list = [tag.strip() for tag in selected_media.tags.split(',')]
            tags_list = sorted(tags_list)
            self.label_tags.set_text(' '.join(tags_list))
        else:
            self.label_tags.set_text('')

        self.label_image.set_image(fr"C:\Storage\Programming\ContentManager_V3\bin\{selected_media.code}")