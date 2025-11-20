import argparse
import ctypes
import os
import random
import sys
from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QScreen, QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QDesktopWidget, QHBoxLayout, \
    QSpacerItem, QSizePolicy, QPushButton

from browser_panel import BrowserPanel
from handler import Media, load_media_from_json
from preview_panel import PreviewPanel
from selector_panel import SelectorPanel
from widgets import Partition


class TopBar(QWidget):
    def __init__(self, player, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

        self.top_font = QFont("Bahnschrift Semibold", 36)

        # Set size
        self.setMinimumSize(1, int(player.min_height / 8))
        self.setMaximumSize(player.min_width, int(player.min_height / 8))

        # --- Layout ---
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # --- Title label ---
        self.title_label = QLabel(f"Media Manager | {player.library_name}")
        self.title_label.setStyleSheet("color: #ffffff; background-color: #141414")
        self.title_label.setFont(self.top_font)
        layout.addWidget(self.title_label)

        # --- Spacer ---
        layout.addStretch()

        # --- Minimize button ---
        self.minimize_button = QPushButton("_")
        self.minimize_button.setFont(self.top_font)
        self.minimize_button.setStyleSheet("""
            QPushButton {color: #ffffff; background-color: #222222; border: none;}
            QPushButton:hover {color: #ff5555;}
            """)
        self.minimize_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.minimize_button.clicked.connect(lambda: self.window().showMinimized())
        layout.addWidget(self.minimize_button)

        # --- Exit button ---
        self.exit_button = QPushButton("✕")
        self.exit_button.setFont(self.top_font)
        self.exit_button.setStyleSheet("""
            QPushButton {color: #ffffff; background-color: #aa1414; border: none;}
            QPushButton:hover {color: #ff5555;}
            """)
        self.exit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.exit_button.clicked.connect(QApplication.quit)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def resizeEvent(self, event):
        self.minimize_button.setFixedSize(self.minimize_button.height(), self.minimize_button.height())
        self.exit_button.setFixedSize(self.exit_button.height(), self.exit_button.height())
        super().resizeEvent(event)

class MainWindow(QMainWindow):
    def __init__(self, media, screen, library_name):
        super().__init__()
        self.media = media
        self.filtered_media = []
        self.media.sort(key=lambda m: m.title)
        self.setWindowTitle("Media Manager")
        self.library_name = library_name

        self.min_width = int(screen.size().width())
        self.min_height = int(screen.size().height())

        self.screen_scale = screen.devicePixelRatio()

        self.setMinimumSize(self.min_width, self.min_height)
        self.showFullScreen()

        self.font_multiplier = self.min_width / 1280

        self.thumb_cache = {}

        self.selected_media = self.media[0]

        central = QWidget()
        self.setCentralWidget(central)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create the top bar
        top_bar = TopBar(self, "#141414")
        layout.addWidget(top_bar, 0, 0, 1, 3)

        # Create a new bar below the top bar
        bottom_bar = Partition("#333333")
        bottom_bar.add_widget(QLabel(""))
        bottom_bar.setMinimumSize(1, int(self.min_height / 12))
        bottom_bar.setMaximumSize(self.min_width, int(self.min_height / 12))
        layout.addWidget(bottom_bar, 1, 0, 1, 3)

        # Create the list menu
        left = BrowserPanel(self, "#222222")
        layout.addWidget(left, 2, 0)

        # Create the selector menu
        self.selector_panel = SelectorPanel(self, "#292929")
        layout.addWidget(self.selector_panel, 2, 1)

        # Create the preview panel
        self.preview_panel = PreviewPanel(self, "#252525", self.selected_media)
        layout.addWidget(self.preview_panel, 2, 2)

        # Stretch factors for columns and rows:
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 8)

        # Setting column stretch to enforce the width percentages:
        layout.setColumnStretch(0, 20)
        layout.setColumnStretch(1, 45)
        layout.setColumnStretch(2, 35)
        central.setLayout(layout)

        QTimer.singleShot(0, lambda: self.filter_media('all', 'all'))

    def get_icon(self, path):
        if path not in self.thumb_cache:
            self.thumb_cache[path] = QIcon(path)
        return self.thumb_cache[path]

    def filter_media(self, item, filter):
        self.filtered_media = [med for med in self.media]

        if filter == 'cast':
            self.filtered_media = [med for med in self.filtered_media if item in med.cast]

        if item == 'All':
            self.filtered_media = [med for med in self.media]

        self.selector_panel.populate_selector()

    def shuffle(self):
        """
        Removes current selection from filtered media list and picks new random media item.
        """
        shuffle_media = self.filtered_media.copy()

        if self.selected_media in shuffle_media:
            shuffle_media.remove(self.selected_media)

        if len(shuffle_media) > 0:
            self.selected_media = random.choice(shuffle_media)

        self.preview_panel.update_panel(self.selected_media)

    def select_previous(self):
        """
        Selects media item left of current selection from filtered media list
        """
        current_index = self.media.index(self.selected_media)
        self.selected_media = self.filtered_media[(current_index - 1) % len(self.filtered_media)]
        self.preview_panel.update_panel(self.selected_media)

    def select_media(self, index):
        """
        Changes currently selected media item
        """
        self.selected_media = [med for med in self.media if med.code == index][0]
        self.preview_panel.update_panel(self.selected_media)

    def select_next(self):
        """
        Selects media item right of current selection from filtered media list
        """
        current_index = self.media.index(self.selected_media)
        self.selected_media = self.filtered_media[(current_index + 1) % len(self.filtered_media)]
        self.preview_panel.update_panel(self.selected_media)

    def resizeEvent(self, event):
        super().resizeEvent(event)


def main():
    parser = argparse.ArgumentParser(description='', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-j', '--json_path', type=str, required=True)
    args = parser.parse_args()
    media = load_media_from_json(args.json_path)
    library_name = os.path.basename(args.json_path)

    app = QApplication(sys.argv)
    screen = app.primaryScreen()

    win = MainWindow(media, screen, library_name)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
