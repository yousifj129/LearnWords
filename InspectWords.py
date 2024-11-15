import random
from typing import List, Dict
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout , QPushButton, 
                              QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt
class InspectWordsWindow(QMainWindow):
    def __init__(self, learned_words: Dict, mainWind):
        super().__init__()
        self.setWindowTitle("Inspect Words")
        self.setMinimumSize(900, 600)
        self.setMaximumSize(1260,720)
        self.learned_words = learned_words
        self.mainWind = mainWind
        # Create the main layout
        main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(main_layout)

        # Create the list of learned words
        self.word_list = QListWidget()
        self.word_list.setSelectionMode(QListWidget.SingleSelection)
        self.word_list.itemDoubleClicked.connect(self.delete_word)
        main_layout.addWidget(self.word_list)

        # Create the buttons
        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear All")
        clear_button.clicked.connect(self.clear_all_words)
        button_layout.addWidget(clear_button)
        main_layout.addLayout(button_layout)

        # Populate the word list
        self.populate_word_list()

    def populate_word_list(self):
        self.word_list.clear()
        for word, info in self.learned_words.items():
            item = QListWidgetItem(f"{word} - {info["definition"]}")
            item.setData(Qt.UserRole, word)
            self.word_list.addItem(item)

    def delete_word(self, item: QListWidgetItem):
        word = item.data(Qt.UserRole)
        del self.learned_words[word]
        self.word_list.takeItem(self.word_list.row(item))
        self.mainWind.save_words()

    def clear_all_words(self):
        self.learned_words.clear()
        self.populate_word_list()
        self.mainWind.save_words()