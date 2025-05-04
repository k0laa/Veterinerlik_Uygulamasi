import hashlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QLineEdit, QLabel, QGridLayout, QWidget
from ui.styles import SAVE_BTN_STYLE, EDIT_BTN_STYLE, DOCTOR_STYLE_INFO
from ui.widgets.hayvan_karti import HayvanKartiWidget
from ui.windows.owner_window_ui import setup_ui
from Windows.add_pet_window import AddPetWindow


class PatientOwnerWindow(QMainWindow):
    def __init__(self, db, user_data):
        super().__init__()

        # Daha sonra kullanılacak olan UI bileşenlerini tanımlama
        self.pets_tab = None
        self.hayvan_main_layout = None
        self.add_pet_window = None
        self.hayvan_kart_layout = None
        self.cancel_button = None
        self.edit_button = None
        self.show_password_button = None
        self.password_confirm = None
        self.new_password = None
        self.exist_password = None
        self.username = None
        self.phone = None
        self.email = None
        self.tc_id = None
        self.first_name = None

        self.db = db
        self.user_data = user_data

        setup_ui(self)
        self.load_profile()

    def load_profile(self):
        """Kullanıcı profilini yükler ve arayüze yerleştir"""
        self.user_data = self.db.get_user_profile(self.user_data['id'])
        if self.user_data:
            self.first_name.setText(self.user_data['name'])
            self.tc_id.setText(self.user_data['tc'])
            self.email.setText(self.user_data['email'])
            self.phone.setText(self.user_data['phone'])
            self.username.setText(self.user_data['username'])
        else:
            QMessageBox.warning(self, "Uyarı", "Profil bilgileri yüklenemedi.")

    def edit_profile(self):
        """Kullanıcı profilini günceller"""
        try:
            updateData = [self.user_data['id']]

            name = self.first_name.text().strip()
            tc = self.tc_id.text().strip()
            email = self.email.text().strip()
            phone = self.phone.text().strip()
            username = self.username.text().strip()
            exist_password = self.exist_password.text().strip()
            new_password = self.new_password.text().strip()
            password_confirm = self.password_confirm.text().strip()

            # Alanların doğruluğunu kontrol et
            if not name:
                QMessageBox.warning(self, "Uyarı", "Ad Soyad alanı boş olamaz.")
                return

            if not tc or len(tc) != 11 or not tc.isdigit():
                QMessageBox.warning(self, "Uyarı", "TC Kimlik No alanı boş olamaz ve 11 haneli bir sayı olmalıdır.")
                return

            if not email or "@" not in email or "." not in email:
                QMessageBox.warning(self, "Uyarı", "Geçerli bir e-posta adresi giriniz.")
                return

            if not phone or len(phone) != 11 or not phone.isdigit():
                QMessageBox.warning(self, "Uyarı", "Telefon numarası 11 haneli bir sayı olmalıdır.")
                return

            if not username:
                QMessageBox.warning(self, "Uyarı", "Kullanıcı adı alanı boş olamaz.")
                return

            # Şifre doğrulama
            hashed_new_password = None  # Varsayılan olarak eski şifreyi koru
            if exist_password or new_password or password_confirm:
                if not exist_password:
                    QMessageBox.warning(self, "Uyarı", "Mevcut şifreyi giriniz.")
                    return

                hashed_exist_password = hashlib.sha256((exist_password + self.user_data['tuz']).encode()).hexdigest()
                if hashed_exist_password != self.user_data['hash']:
                    QMessageBox.warning(self, "Uyarı", "Mevcut şifre yanlış.")
                    return

                if new_password != password_confirm:
                    QMessageBox.warning(self, "Uyarı", "Yeni şifreler eşleşmiyor.")
                    return

                if len(new_password) <= 6:
                    QMessageBox.warning(self, "Uyarı", "Yeni şifre en az 6 karakter uzunluğunda olmalıdır.")
                    return

                hashed_new_password = new_password

            # Güncelleme verilerini hazırla
            updateData.extend([name, tc, email, phone, username, hashed_new_password])

            # Veritabanını güncelle
            if not self.db.update_user_profile(*updateData):
                QMessageBox.warning(self, "Uyarı", "Profil güncellenemedi.")
                return

            updatedDatas = []

            if name != self.user_data['name']:
                updatedDatas.append(f"Ad Soyad: {name}")
            if tc != self.user_data['tc']:
                updatedDatas.append(f"TC Kimlik No: {tc}")
            if email != self.user_data['email']:
                updatedDatas.append(f"E-posta: {email}")
            if phone != self.user_data['phone']:
                updatedDatas.append(f"Telefon: {phone}")
            if username != self.user_data['username']:
                updatedDatas.append(f"Kullanıcı Adı: {username}")
            if new_password:
                updatedDatas.append("Şifre: Güncellendi")
            if not updatedDatas:
                updatedDatas.append("Hiçbir bilgi güncellenmedi.")

            QMessageBox.information(self, "Başarılı", f"Profil başarıyla güncellendi. \n Değiştirilen bilgiler: {', '.join(updatedDatas)}")
            self.load_profile()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")

    def load_pets(self):
        """Kullanıcının hayvanlarını yükler ve tabloya yerleştirir"""
        # Mevcut kartları temizle
        if hasattr(self, 'hayvan_kart_layout'):
            while self.hayvan_kart_layout.count():
                child = self.hayvan_kart_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        pets = self.db.get_pets(self.user_data['id'])
        if pets:
            for i, hayvan_data in enumerate(pets):
                hayvan_karti = HayvanKartiWidget(hayvan_data)
                y = i // 3
                self.hayvan_kart_layout.addWidget(hayvan_karti, y, i % 3, alignment=Qt.AlignLeft)
                hayvan_karti.delete_btn.clicked.connect(lambda a: self.delete_pet(hayvan_karti.pet_id))
                hayvan_karti.edit_btn.clicked.connect(lambda a: self.edit_pets(hayvan_karti.pet_id))
        else:
            no_patient_label = QLabel("Hayvanınız bulunmamaktadır.")
            no_patient_label.setObjectName("info")
            no_patient_label.setStyleSheet(DOCTOR_STYLE_INFO)
            no_patient_label.setAlignment(Qt.AlignCenter)
            self.hayvan_kart_layout.addWidget(no_patient_label)

    def edit_pets(self, pet_id):
        """Hayvanları düzenlemek için pencere açar"""
        pet = self.db.get_pet(pet_id)
        self.add_pet_window = AddPetWindow(self.db, pet, self.user_data['id'])  # Referansı sakla
        self.add_pet_window.show()
        self.add_pet_window.closeEvent = lambda event: self.load_pets()

    def add_new_pet(self):
        """Yeni bir hayvan eklemek için pencere açar"""
        self.add_pet_window = AddPetWindow(self.db, None, self.user_data['id'])  # Referansı sakla
        self.add_pet_window.show()
        self.add_pet_window.closeEvent = lambda event: self.load_pets()

    def delete_pet(self, pet_id):
        """Seçilen hayvanı siler"""
        self.db.delete_pet(pet_id)
        self.load_pets()  # Hayvan silindikten sonra tabloyu güncelle

    def load_appointments(self):

        """Kullanıcının randevularını yükler ve tabloya yerleştirir"""
        appointments = self.db.get_user_appointments(self.user_data['id'])
        if appointments:
            self.appointments_table.setRowCount(len(appointments))
            for i, appointment in enumerate(appointments):
                self.appointments_table.setItem(i, 0, QTableWidgetItem(appointment['date']))
                self.appointments_table.setItem(i, 1, QTableWidgetItem(appointment['time']))
                self.appointments_table.setItem(i, 2, QTableWidgetItem(appointment['vet']))
                self.appointments_table.setItem(i, 3, QTableWidgetItem(appointment['status']))
        else:
            print("Randevu bilgileri yüklenemedi.")
            self.appointments_table.setRowCount(0)
            self.appointments_table.setColumnCount(4)
            self.appointments_table.setHorizontalHeaderLabels(["Tarih", "Saat", "Veteriner", "Durum"])

    def add_appointment(self):
        """Yeni bir randevu almak için pencere açar"""
        from Windows.add_appointment_window import AddAppointmentWindow
        add_appointment_window = AddAppointmentWindow(self.db, self.user_data)
        add_appointment_window.exec_()
        self.load_appointments()  # Randevu alındıktan sonra tabloyu güncelle

    def update_pet(self):
        """Seçilen hayvanı günceller"""
        selected_row = self.pets_table.currentRow()
        if selected_row >= 0:
            pet_name = self.pets_table.item(selected_row, 0).text()  # from Windows.update_pet_window import UpdatePetWindow  # update_pet_window = UpdatePetWindow(self.db, pet_name)  # update_pet_window.exec_()  # self.load_pets()
        else:
            print("Güncellenecek hayvan seçilmedi.")

    def toggle_password(self):
        """Şifre görünürlüğünü değiştirirme"""
        if self.new_password.echoMode() == QLineEdit.Password:
            self.new_password.setEchoMode(QLineEdit.Normal)
            self.password_confirm.setEchoMode(QLineEdit.Normal)
            self.exist_password.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText("Şifreyi Gizle")
        else:
            self.new_password.setEchoMode(QLineEdit.Password)
            self.password_confirm.setEchoMode(QLineEdit.Password)
            self.exist_password.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("Şifreyi Göster")

    def toggle_edit(self):
        """Düzenleme modunu aç/kapat"""
        try:
            is_read_only = self.first_name.isReadOnly()
            self.first_name.setReadOnly(not is_read_only)
            self.tc_id.setReadOnly(not is_read_only)
            self.email.setReadOnly(not is_read_only)
            self.phone.setReadOnly(not is_read_only)
            self.username.setReadOnly(not is_read_only)
            self.exist_password.setReadOnly(not is_read_only)
            self.new_password.setReadOnly(not is_read_only)
            self.password_confirm.setReadOnly(not is_read_only)

            if is_read_only:
                self.edit_button.setText("Kaydet")
                self.edit_button.setStyleSheet(SAVE_BTN_STYLE)
                self.cancel_button.setVisible(True)
            else:
                self.edit_button.setText("Düzenle")
                self.edit_button.setStyleSheet(EDIT_BTN_STYLE)
                self.edit_profile()
                self.cancel_button.setVisible(False)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")

    def cancel_edit(self):
        """Düzenleme modunu iptal et"""
        self.first_name.setReadOnly(True)
        self.tc_id.setReadOnly(True)
        self.email.setReadOnly(True)
        self.phone.setReadOnly(True)
        self.username.setReadOnly(True)
        self.exist_password.setReadOnly(True)
        self.new_password.setReadOnly(True)
        self.password_confirm.setReadOnly(True)

        self.edit_button.setText("Düzenle")
        self.edit_button.setStyleSheet(EDIT_BTN_STYLE)
        self.cancel_button.setVisible(False)
