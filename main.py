import sys
from PyQt5.QtWidgets import QApplication
from Windows.veteriner_app import VeterinerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VeterinerApp()
    window.show()
    sys.exit(app.exec_())