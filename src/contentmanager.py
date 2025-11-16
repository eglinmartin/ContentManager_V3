import random
import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QDesktopWidget

from handler import Media
from preview_panel import PreviewPanel
from widgets import Partition


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Content Manager")

        screen_geometry = QDesktopWidget().availableGeometry()
        self.resize(int(screen_geometry.width() * 0.8), int(screen_geometry.height() * 0.8))
        self.showMaximized()

        self.media = [
            Media('Indiana Jones and the Raiders of the Lost Ark', 'Steven Spielberg', ['Harrison Ford', 'Karen Allen', 'Paul Freeman'], 0, datetime(1981, 1, 1), 'Movie', ['favourite']),
            Media('Indiana Jones and the Temple of Doom', 'Steven Spielberg', ['Harrison Ford', 'Kate Capshaw', 'Ke Huy Quan'], 1, datetime(1981, 1, 1), 'Movie', ['favourite']),
            Media('Indiana Jones and the Last Crusade', 'Steven Spielberg', ['Harrison Ford', 'Sean Connery', 'Denholm Elliott'], 2, datetime(1981, 1, 1), 'Movie', ['favourite']),
            Media('Indiana Jones and the Kingdom of the Crystal Skull', 'Steven Spielberg', ['Harrison Ford', 'Cate Blanchett', 'Karen Allen'], 3, datetime(1981, 1, 1), 'Movie', ['favourite']),
            Media('Indiana Jones and the Dial of Destiny', 'James Mangold', ['Harrison Ford', 'Phoebe Waller-Bridge', 'Antonio Banderas'], 4, datetime(1981, 1, 1), 'Movie', ['favourite']),
        ]
        self.selected_media = self.media[2]

        central = QWidget()
        self.setCentralWidget(central)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create the top bar
        top = Partition("#141414")
        top.add_widget(QLabel("Top Bar Content"))
        top.setMinimumSize(1, 100)
        layout.addWidget(top, 0, 0, 1, 3)

        # Create the list menu
        left = Partition("#222222")
        layout.addWidget(left, 1, 0)

        # Create the selector menu
        middle = Partition("#292929")
        layout.addWidget(middle, 1, 1)

        # Create the preview panel
        self.preview_panel = PreviewPanel(self, "#252525", self.selected_media)
        layout.addWidget(self.preview_panel, 1, 2)

        # Stretch factors for columns and rows:
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 9)

        # Setting column stretch to enforce the width percentages:
        layout.setColumnStretch(0, 25)
        layout.setColumnStretch(1, 45)
        layout.setColumnStretch(2, 30)

        central.setLayout(layout)

    def shuffle(self):
        shuffle_media = self.media.copy()
        shuffle_media.remove(self.selected_media)
        self.selected_media = random.choice(shuffle_media)
        self.preview_panel.update_panel(self.selected_media)

    def select_previous(self):
        current_index = self.media.index(self.selected_media)
        self.selected_media = self.media[(current_index - 1) % len(self.media)]
        self.preview_panel.update_panel(self.selected_media)

    def select_next(self):
        current_index = self.media.index(self.selected_media)
        self.selected_media = self.media[(current_index + 1) % len(self.media)]
        self.preview_panel.update_panel(self.selected_media)

    def resizeEvent(self, event):
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
