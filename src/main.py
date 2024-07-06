# main.py

from gui import StrassenGUI
import sys
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StrassenGUI()
    window.show()
    sys.exit(app.exec())