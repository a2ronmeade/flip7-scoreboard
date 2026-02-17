from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from themes import LIGHT_THEME, DARK_THEME

class SettingsWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__(flags=Qt.Window)
        self.setWindowTitle("Settings")
        self.resize(400, 300)

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

        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.setChecked(True)
        self.dark_mode_checkbox.stateChanged.connect(self.update_theme)
        layout.addWidget(self.dark_mode_checkbox)

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

        layout.addStretch()

    def update_theme(self, state):
        self.current_theme = "Dark" if state == Qt.Checked else "Light"

    def update_font(self, text):
        self.font_size = text

    def closeEvent(self, event):
        if self.main_window:
            # Apply theme
            if self.current_theme == "Dark":
                self.main_window.setStyleSheet(DARK_THEME)
            else:
                self.main_window.setStyleSheet(LIGHT_THEME)

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
