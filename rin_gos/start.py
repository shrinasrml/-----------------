import sys

from PySide6.QtWidgets import QApplication

from controller import MainWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWidget()
    window.show()

    sys.exit(app.exec())
