from email.mime import text
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from themes import LIGHT_THEME, DARK_THEME, SPRING_THEME, SUMMER_THEME, AUTUMN_THEME, WINTER_THEME

class SettingsWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__(flags=Qt.Window)
        self.setWindowTitle("Settings")
        self.resize(400, 300)
        self.setStyleSheet(DARK_THEME)
        
        self.main_window = main_window

        # default settings
        self.WINNING_THRESHOLD = 200
        self.current_theme = "Dark"
        self.font_size = "Regular"

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Theme selection
        theme_label = QLabel("Theme:")
        layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark","Light","Spring","Summer","Autumn","Winter"])
        self.theme_combo.setCurrentText(self.current_theme)
        self.theme_combo.currentTextChanged.connect(self.update_theme)
        layout.addWidget(self.theme_combo)

        # Winning Threshold
        threshold_layout = QHBoxLayout()
        threshold_label = QLabel("Winning Threshold:")
        self.threshold_input = QLineEdit(str(self.WINNING_THRESHOLD))
        self.threshold_input.setFixedWidth(100)
        threshold_layout.addWidget(threshold_label)
        threshold_layout.addWidget(self.threshold_input)
        layout.addLayout(threshold_layout)

        # Font size
        font_label = QLabel("Font Size:")
        layout.addWidget(font_label)

        self.font_combo = QComboBox()
        self.font_combo.addItems(["Regular", "Large", "Extra Large"])
        self.font_combo.setCurrentText(self.font_size)
        self.font_combo.currentTextChanged.connect(self.update_font)
        layout.addWidget(self.font_combo)

        self.reset_button = QPushButton("Reset Game")
        self.reset_button.clicked.connect(self.reset_game)
        layout.addWidget(self.reset_button)

        layout.addStretch()

    def update_theme(self, text):
        self.current_theme = text

    def update_font(self, text):
        self.font_size = text

    def closeEvent(self, event):
        if self.main_window:
            # Apply theme
            theme_map = {
                "Dark": DARK_THEME,
                "Light": LIGHT_THEME,
                "Spring": SPRING_THEME,
                "Summer": SUMMER_THEME,
                "Autumn": AUTUMN_THEME,
                "Winter": WINTER_THEME,
            }

            selected_theme = theme_map.get(self.current_theme, DARK_THEME)
            self.main_window.setStyleSheet(selected_theme)

            font_map = {"Regular": 30, "Large": 38, "Extra Large": 46}
            size = font_map.get(self.font_size, 30)
    
            self.main_window.setStyleSheet(
                self.main_window.styleSheet() + f" QWidget {{ font-size: {size}px; }}"
            )

            # update winning threshold
            if hasattr(self.main_window, "WINNING_THRESHOLD"):
                try:
                    self.main_window.WINNING_THRESHOLD = int(self.threshold_input.text())
                except ValueError:
                    self.main_window.WINNING_THRESHOLD = 200

        event.accept()

    def reset_game(self):
        if self.main_window:
            self.main_window.reset_game()
