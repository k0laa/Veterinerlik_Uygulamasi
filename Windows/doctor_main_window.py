from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QLabel
from PyQt5.QtCore import Qt
from ui.doctor_main_window_ui import setup_ui
from ui.styles import DOCTOR_STYLE_INFO
from ui.widgets.hasta_karti import HastaKartiWidget
from Windows.appointment_window import OppointmentWindow


class DoctorWindow(QMainWindow):
    def __init__(self, database, user_data):
        super().__init__()
        self.randevu_elements = None
        self.search_combo = None
        self.search_input = None
        self.bekleyen_content = None
        self.rapor_table = None
        self.oppointment_window = None
        self.icon_path = None
        self.toolbar = None
        self.database = database
        self.user_data = user_data
        self.setup_ui()

    def setup_ui(self):
        # UI kurulumu
        setup_ui(self)

        # Başlangıçta verileri yükle
        self.refresh_data()  #

    def refresh_data(self):
        self.refresh_rapor()
        self.refresh_bekleyen_hastalar()

    def refresh_rapor(self):
        """Rapor tablosunu ve istatistikleri günceller"""
        if hasattr(self, 'rapor_table'):
            records = self.database.get_all_patients()
            self.rapor_table.setRowCount(len(records))

            for i, record in enumerate(records):
                self.rapor_table.setItem(i, 0, QTableWidgetItem(str(record[0])))  # ID
                self.rapor_table.setItem(i, 1, QTableWidgetItem(record[1]))  # Hayvan Adı
                self.rapor_table.setItem(i, 2, QTableWidgetItem(record[2]))  # Sahip Adı
                self.rapor_table.setItem(i, 3, QTableWidgetItem(record[3]))  # Tür
                self.rapor_table.setItem(i, 4, QTableWidgetItem(record[4]))  # Cins
                self.rapor_table.setItem(i, 5, QTableWidgetItem(record[5]))  # Cinsiyet
                self.rapor_table.setItem(i, 6, QTableWidgetItem(str(record[6])))  # Yaş
                self.rapor_table.setItem(i, 7, QTableWidgetItem(record[7]))  # Durum
                self.rapor_table.setItem(i, 8, QTableWidgetItem(str(record[8])))  # İlerleme
                self.rapor_table.setItem(i, 9, QTableWidgetItem(record[9]))  # Açıklama
                self.rapor_table.setItem(i, 10, QTableWidgetItem(record[10]))  # İlaçlar
                self.rapor_table.setItem(i, 11, QTableWidgetItem(record[11]))  # Eklenme Tarihi

            # İstatistikleri güncelle
            stats = self.database.get_statistics()
            if hasattr(self, 'stat_cards'):
                self.stat_cards['total_patients'].findChild(QLabel, "value_label").setText(str(stats['total']))
                self.stat_cards['treatment_success'].findChild(QLabel, "value_label").setText(f"{stats['success_rate']:.1f}%")

    def refresh_bekleyen_hastalar(self):
        """Bekleyen hastaları günceller"""
        try:
            if not hasattr(self, 'bekleyen_content'):
                return

            records = self.database.get_waiting_patients()
            content_layout = self.bekleyen_content.layout()

            # Mevcut kartları temizle
            while content_layout.count():
                child = content_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Yeni kartları ekle
            if records:
                for record in records:
                    # Hasta kartını oluştur
                    hasta_karti = HastaKartiWidget(record, self.bekleyen_content)
                    content_layout.addWidget(hasta_karti)
            else:
                no_patient_label = QLabel("Şu anda bekleyen hasta bulunmamaktadır.")
                no_patient_label.setObjectName("info")
                no_patient_label.setStyleSheet(DOCTOR_STYLE_INFO)
                no_patient_label.setAlignment(Qt.AlignCenter)
                content_layout.addWidget(no_patient_label)

            # Kartların altına boşluk ekle
            content_layout.addStretch()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bekleyen hastalar güncellenirken hata: {str(e)}")

    def delete_record(self):
        """Seçili kaydı siler"""
        # Yetki kontrolü
        if not self.user_data['yetkiler']['hasta_sil']:
            QMessageBox.warning(self, "Yetkisiz İşlem", "Bu işlem için yetkiniz bulunmamaktadır!")
            return

        try:
            current_row = self.rapor_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Uyarı", "Lütfen silinecek bir kayıt seçin!")
                return

            # Seçili kaydın ID'sini al
            record_id = self.rapor_table.item(current_row, 0).text()
            reply = QMessageBox.question(self, "Onay", "Bu kaydı silmek istediğinizden emin misiniz?", QMessageBox.Yes | QMessageBox.No)

            # Eğer kullanıcı "Evet" derse kaydı sil
            if reply == QMessageBox.Yes:
                if self.database.delete_patient(record_id):
                    self.refresh_data()
                    QMessageBox.information(self, "Başarılı", "Kayıt başarıyla silindi!")
                else:
                    QMessageBox.critical(self, "Hata", "Kayıt silinirken bir hata oluştu!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt silme hatası: {str(e)}")

    def filter_reports(self):
        """Raporları filtreler"""
        try:
            # Seçili filtreleme kriterini al
            text = self.search_input.text().lower()

            for row in range(self.rapor_table.rowCount()):
                column = self.search_combo.currentIndex() + 1
                item = self.rapor_table.item(row, column)

                # item.text() i içermiyorsa satırı gizle, aksi takdirde göster
                self.rapor_table.setRowHidden(row, text not in item.text().lower() if item else True)
        except Exception as e:
            print(f"Filtreleme hatası: {e}")

    def edit_record(self):
        """Seçili kaydı hasta kayıt formuna aktarır"""
        try:
            current_row = self.rapor_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Uyarı", "Lütfen düzenlenecek bir kayıt seçin!")
                return

            # Seçili kaydın ID'sini al
            record_id = int(self.rapor_table.item(current_row, 0).text())

            # Hasta kayıt formunu aç
            self.oppointment_window = OppointmentWindow(self.database, self.user_data, record_id, self)
            self.oppointment_window.show()
            self.oppointment_window.edit_record()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt düzenleme hatası: {str(e)}")