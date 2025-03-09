import sys
from PyQt5.QtWidgets import QApplication
from veteriner_app import VeterinerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VeterinerApp()
    sys.exit(app.exec_())