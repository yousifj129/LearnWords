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
    
    
    settings = {}
    # load settings.json
    with open("settings.json", "r") as f:
        settings = json.load(f)
    print(settings["settings"]["theme"])
    theme = ""
    if settings["settings"]["theme"] == "dark":
        theme = "Windows11"
    elif settings["settings"]["theme"] == "light":
        theme = "windowsvista"
    else:
        theme = "Fusion"


    font = QFont(settings["settings"]["font"], int(settings["settings"]["fontSize"]))
    

    app.setWindowIcon(icon)
    app.setFont(font)
    app.setStyle(QStyleFactory.create(theme))
    window = MainWind()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()