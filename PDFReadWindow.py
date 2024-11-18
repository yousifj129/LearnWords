import random
from typing import List, Dict
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout , QPushButton, 
                              QLabel, QLineEdit, QListWidget, QListWidgetItem, QFileDialog)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from Word import Word
class PDFReadWindow(QMainWindow):
    def __init__(self, learned_words: Dict, mainWind):
        super().__init__()
        self.setWindowTitle("PDF Reader")
        self.setMinimumSize(1200, 800)
        self.learned_words = learned_words
        self.mainWind = mainWind

        # Create the main layout
        main_layout = QHBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(main_layout)

        # Create the PDF viewer
        self.pdf_viewer = QWebEngineView()
        settings = self.pdf_viewer.settings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        main_layout.addWidget(self.pdf_viewer, 3)

        # Create the word panel
        word_panel = QVBoxLayout()
        main_layout.addLayout(word_panel, 1)

        # Add a new word input
        new_word_layout = QHBoxLayout()
        new_word_label = QLabel("New Word:")
        self.new_word_input = QLineEdit()
        self.new_word_input.returnPressed.connect(self.add_new_word)
        new_word_layout.addWidget(new_word_label)
        new_word_layout.addWidget(self.new_word_input)
        word_panel.addLayout(new_word_layout)

        # Add the word list
        self.word_list = QListWidget()
        self.word_list.itemDoubleClicked.connect(self.show_word_details)
        word_panel.addWidget(self.word_list)

        self.show_file_dialog()
    def show_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            self.load_pdf(selected_file)

    def load_pdf(self, file_path: str):
        self.pdf_viewer.load(QUrl(file_path))

    def add_new_word(self):
        word = self.new_word_input.text().strip()
        if word:
            if word not in self.learned_words:
                self.mainWind.add_word_out(word)
                self.populate_word_list()
            self.new_word_input.clear()

    def populate_word_list(self):
        self.word_list.clear()
        for word, info in self.learned_words.items():
            item = QListWidgetItem(word)
            item.setData(Qt.UserRole, word)
            self.word_list.addItem(item)

    def show_word_details(self, item: QListWidgetItem):
        word = item.data(Qt.UserRole)
        word_data = self.learned_words[word]
        # Display the word details in a new window or dialog
        print(word_data)