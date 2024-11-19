import sys
import json
import random
from pathlib import Path
from typing import List, Dict
from PySide6.QtWidgets import (QApplication,QStyleFactory)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from MainWind import MainWind
from PySide6.QtGui import QIcon,QColor,QPalette

def main():
    app = QApplication(sys.argv)
    icon = QIcon("imgs/ICON.png")
    app.setWindowIcon(icon)
    font = QFont("Arial", 15)
    app.setFont(font)
    print(QStyleFactory.keys())
    app.setStyle(QStyleFactory.create("windows11"))
    window = MainWind()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()