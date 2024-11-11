import sys
import json
import random
from pathlib import Path
from typing import List, Dict
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLineEdit, QPushButton, QTextEdit, 
                              QLabel, QMessageBox, QRadioButton, QButtonGroup)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from MainWind import VocabularyApp

def main():
    app = QApplication(sys.argv)
    font = QFont("Arial", 15)
    app.setFont(font)
    window = VocabularyApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()