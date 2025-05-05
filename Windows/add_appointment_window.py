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
        pet_id = self.ad_combo.currentData()
        date = self.tarih_input.date().toString("yyyy-MM-dd")
        time = self.saat_input.time().toString("HH:mm")

        appointment_data = {'pet_id':pet_id,
                            'tarih': date,
                            'saat': time}

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

