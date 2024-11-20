from pathlib import Path
import sys
import json
from PySide6.QtWidgets import (QApplication,QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel
                               , QSpinBox, QComboBox, QPushButton,QStyleFactory,QLineEdit,QFileDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase,QFont

class SettingsWindow(QMainWindow):
    def __init__(self,app :QApplication,mainwind):
        
        super().__init__()
        self.setWindowTitle("Settings")
        self.app = app
        self.mainwind = mainwind
        # Load settings from file
        with open("settings.json", "r") as f:
            self.settings = json.load(f)

        # Create the main layout
        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(layout)

        # Theme dropdown
        theme_label = QLabel("Theme:")
        self.theme_dropdown = QComboBox()
        self.theme_dropdown.addItems(["dark", "light", "system", "fusion"])
        self.theme_dropdown.setCurrentText(self.settings["theme"])
        self.theme_dropdown.currentTextChanged.connect(self.update_settings)
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_dropdown)

        # Font size spinbox
        font_size_label = QLabel("Font Size:")
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setMinimum(8)
        self.font_size_spinbox.setMaximum(24)
        self.font_size_spinbox.setValue(int(self.settings["fontSize"]))
        self.font_size_spinbox.valueChanged.connect(self.update_settings)
        layout.addWidget(font_size_label)
        layout.addWidget(self.font_size_spinbox)

        # Font family dropdown
        font_family_label = QLabel("Font Family:")
        self.font_family_dropdown = QComboBox()
        font_families = QFontDatabase.families()
        self.font_family_dropdown.addItems(font_families)
        self.font_family_dropdown.setCurrentText(self.settings["font"])
        self.font_family_dropdown.currentTextChanged.connect(self.update_settings)
        layout.addWidget(font_family_label)
        layout.addWidget(self.font_family_dropdown)

        # Words file chooser (open a file dialog to select the words file)
        words_file_label = QLabel("Words File:")
        self.words_file_edit = QLineEdit(self.settings["wordsFile"])
        self.words_file_button = QPushButton("Browse")
        self.words_file_button.clicked.connect(self.update_settings)
        layout.addWidget(words_file_label)
        layout.addWidget(self.words_file_edit)
        layout.addWidget(self.words_file_button)

        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        self.setLayout(layout)
        
    def update_settings(self):
        if self.sender() == self.theme_dropdown:
            self.settings["theme"] = self.theme_dropdown.currentText()
            theme = ""
            if self.settings["theme"] == "dark":
                theme = "Windows11"
            elif self.settings["theme"] == "light":
                theme = "windowsvista"
            elif self.settings["theme"] == "system":
                theme = ""
            else:
                theme = "Fusion"
            self.app.setStyle(QStyleFactory.create(theme))
        elif self.sender() == self.font_size_spinbox:
            self.settings["fontSize"] = self.font_size_spinbox.value()
            self.app.setFont(QFont(self.settings["font"], self.settings["fontSize"]))
        elif self.sender() == self.font_family_dropdown:
            self.settings["font"] = self.font_family_dropdown.currentText()
            self.app.setFont(QFont(self.settings["font"], self.settings["fontSize"]))
        elif self.sender() == self.words_file_button:
            # open a file dialog to select the words file (json or txt)
            words_file, _ = QFileDialog.getOpenFileName(self, "Select Words File", "", "JSON and Text Files (*.json *.txt)")
            if words_file:
                self.settings["wordsFile"] = words_file
                self.words_file_edit.setText(words_file)
                self.mainwind.words_file = Path(words_file)
                self.mainwind.learned_words = self.mainwind.load_words()
            
    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)
        self.close()
        