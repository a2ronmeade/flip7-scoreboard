import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from settings import SettingsWindow
from themes import LIGHT_THEME, DARK_THEME

class Player:
    def __init__(self, name):
        self.name = name
        self.total_score = 0
        self.round_score = 0

class Scoreboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scoreboard")
        self.resize(600, 500)
        self.setStyleSheet(DARK_THEME)

        self.players = []
        self.player_widgets = {}

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)
        top_layout.addStretch()

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setFixedWidth(self.width() // 2) # same thing as above
        top_layout.addWidget(self.settings_button)
        top_layout.addStretch()

        self.add_player_button = QPushButton("Add Player")
        self.add_player_button.clicked.connect(self.add_player)
        self.add_player_button.setFixedWidth(self.width() // 2)  # middle third bc it looks nice
        top_layout.addWidget(self.add_player_button)
        top_layout.addStretch()

        

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        self.player_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.player_layout)

        self.next_round_button = QPushButton("Next Round")
        self.next_round_button.clicked.connect(self.next_round)
        main_layout.addWidget(self.next_round_button)

    def add_player(self):
        name, ok = QInputDialog.getText(self, "Add Player", "Enter player name:")
        if ok and name:
            player = Player(name)
            self.players.append(player)
            self.create_player_row(player)

    def create_player_row(self, player):
        row = QHBoxLayout()
        name_label = QLabel(player.name)
        name_label.setFixedWidth(150)
        row.addWidget(name_label)

        total_label = QLabel(str(player.total_score))
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setFixedWidth(100)
        row.addWidget(total_label)

        round_input = QLineEdit()
        round_input.setFixedWidth(100)
        round_input.setPlaceholderText("0")
        row.addWidget(round_input)

        self.player_layout.addLayout(row)
        self.player_widgets[player] = (total_label, round_input)

    def next_round(self):
        for player in self.players:
            total_label, round_input = self.player_widgets[player]
            try:
                round_score = int(round_input.text())
            except ValueError:
                round_score = 0
            player.total_score += round_score
            round_input.clear()
            total_label.setText(str(player.total_score))

    def open_settings(self):
        self.settings_window = SettingsWindow(main_window=self)
        self.settings_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Scoreboard()
    window.show()
    sys.exit(app.exec_())
