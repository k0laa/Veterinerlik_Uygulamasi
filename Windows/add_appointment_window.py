import datetime

from PyQt5.QtWidgets import QMessageBox, QMainWindow
from ui.windows.add_appointment_window_ui import setup_ui


class AddAppointmentWindow(QMainWindow):
    def __init__(self, database, user_data):
        super().__init__()
        self.saat_input = None
        self.tarih_input = None
        self.ad_combo = None
        self.database = database
        self.user_data = user_data

        # UI bileşenlerini ayarla
        self.setup_ui()

    def setup_ui(self):
        setup_ui(self)

    def save_appointment(self):
        """Randevuyu kaydeder."""
        try:
            pet = self.database.get_pet(self.ad_combo.currentData())
            # Form verilerini al
            data = {'hayvan_adi': self.ad_combo.currentText(), 'sahip_adi': self.user_data['name'], 'tur': pet[1], 'cinsiyet': pet[3], 'cins': pet[2], 'yas': pet[5], 'durum': "Muayene Bekliyor", 'ilerleme': 0, 'sikayet': None, 'aciklama': None,
                    'ilaclar': None, 'ekleyen_id': self.user_data['id'], 'tarih': self.tarih_input.date().toString("yyyy-MM-dd"), 'saat': self.saat_input.time().toString("HH:mm")}

            success = self.database.add_patient(data)

            if success:
                QMessageBox.information(self, "Başarılı", "Yeni kayıt başarıyla eklendi.")
            else:
                QMessageBox.warning(self, "Hata", "Kayıt işlemi başarısız oldu!")
        except Exception as e:
            print(f"Kayıt işlemi sırasında hata: {str(e)}")  # Hata ayıklama için
            QMessageBox.critical(self, "Hata", f"Kayıt işlemi sırasında bir hata oluştu: {str(e)}")

        pet_id = self.ad_combo.currentData()
        date = self.tarih_input.date().toString("yyyy-MM-dd")
        time = self.saat_input.time().toString("HH:mm")  #
        appointment_data = {'pet_id': pet_id, 'tarih': date, 'saat': time}

        # Veritabanına randevu ekle
        if self.database.add_appointment(appointment_data):
            QMessageBox.information(self, "Başarılı", "Randevu başarıyla eklendi.")
            self.close_win()
        else:
            QMessageBox.warning(self, "Hata", "Randevu eklenirken bir hata oluştu.")

    def get_pets(self):
        """Kullanıcının hayvanlarını alır."""
        return self.database.get_pets(self.user_data[0])

    def close_win(self):
        """Pencereyi kapatır."""
        self.close()
