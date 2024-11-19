import random
from typing import List, Dict
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, 
                              QLabel, QLineEdit, QTextEdit, QListWidgetItem, QFileDialog, QToolBar, QSplitter)
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
        main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(main_layout)

        # Create the splitter
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)

        # Create the left layout (PDF viewer)
        left_layout = QVBoxLayout()
        self.toolbar = QToolBar()
        self.toolbar.addAction("Open PDF", self.show_file_dialog)
        left_layout.addWidget(self.toolbar, 0, alignment=Qt.AlignmentFlag.AlignTop)

        self.pdf_viewer = QWebEngineView()
        settings = self.pdf_viewer.settings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        left_layout.addWidget(self.pdf_viewer, 3)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        self.splitter.addWidget(left_widget)

        # Create the right layout (word panel)
        right_layout = QVBoxLayout()
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        self.splitter.addWidget(right_widget)

        # Add a new word input
        new_word_layout = QHBoxLayout()
        new_word_label = QLabel("New Word:")
        self.new_word_input = QLineEdit()
        self.new_word_input.returnPressed.connect(self.add_new_word)
        new_word_layout.addWidget(new_word_label)
        new_word_layout.addWidget(self.new_word_input)
        right_layout.addLayout(new_word_layout)

        self.display_area = QTextEdit()
        self.display_area.setReadOnly(True)
        right_layout.addWidget(self.display_area)

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
            self.mainWind.add_word_out(word)
            self.display_word_info(word)

            self.new_word_input.clear()

    def display_word_info(self, word: str):
        """Display word information in the text area."""
        word_info = self.learned_words[word]
        definition_str = ""
        example_str = ""
        for defin in word_info['definition']:
            definition_str += '- ' + defin + '\n'
        for ex in word_info['examples']:
            example_str += '- ' + ex + '\n'
        # Format the information
        display_text = f"Word: {word}\n"
        display_text += f"Phonetic: {word_info['phonetic']}\n\n"
        display_text += f"Definitions: \n{definition_str}\n\n"
        display_text += f"Examples: \n{example_str}\n\n"
        if word_info['synonyms']:
            display_text += f"Synonyms: {', '.join(word_info['synonyms'])}\n"
        if word_info['antonyms']:
            display_text += f"Antonyms: {', '.join(word_info['antonyms'])}\n"
        self.display_area.setText(display_text)