import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
import sqlite3


class VeterinerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veterinerlik Uygulaması")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()
        self.initDB()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Veterinerlik Yönetim Sistemi", self)
        self.button_add = QPushButton("Hasta Ekle", self)
        self.button_show = QPushButton("Hasta Kayıtlarını Görüntüle", self)
        self.button_appointment = QPushButton("Randevu Ekle", self)

        self.button_add.clicked.connect(self.add_patient)
        self.button_show.clicked.connect(self.show_patients)
        self.button_appointment.clicked.connect(self.add_appointment)

        layout.addWidget(self.label)
        layout.addWidget(self.button_add)
        layout.addWidget(self.button_show)
        layout.addWidget(self.button_appointment)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def initDB(self):
        self.conn = sqlite3.connect("veteriner.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS hastalar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hayvan_adi TEXT NOT NULL,
                tur TEXT NOT NULL,
                yas INTEGER,
                sahip TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS randevular (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hasta_id INTEGER,
                tarih TEXT,
                saat TEXT,
                FOREIGN KEY (hasta_id) REFERENCES hastalar (id)
            )
        """)
        self.conn.commit()

    def add_patient(self):
        hayvan_adi, tur, yas, sahip = "Köpük", "Köpek", 3, "Ahmet Yılmaz"
        self.cursor.execute("INSERT INTO hastalar (hayvan_adi, tur, yas, sahip) VALUES (?, ?, ?, ?)", (hayvan_adi, tur, yas, sahip))
        self.conn.commit()
        QMessageBox.information(self, "Başarılı", "Hasta başarıyla eklendi!")

    def show_patients(self):
        self.cursor.execute("SELECT * FROM hastalar")
        records = self.cursor.fetchall()

        self.table.setRowCount(len(records))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Hayvan Adı", "Tür", "Sahip"])

        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def add_appointment(self):
        hasta_id, tarih, saat = 1, "2025-03-10", "14:00"
        self.cursor.execute("INSERT INTO randevular (hasta_id, tarih, saat) VALUES (?, ?, ?)", (hasta_id, tarih, saat))
        self.conn.commit()
        QMessageBox.information(self, "Başarılı", "Randevu başarıyla eklendi!")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VeterinerApp()
    window.show()
    sys.exit(app.exec_())
