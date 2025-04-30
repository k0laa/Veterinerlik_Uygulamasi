from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from ui.owner_window_ui_2 import setup_ui


class PatientOwnerWindow(QMainWindow):
    def __init__(self, db, user_data):
        super().__init__()
        self.db = db
        self.user_data = user_data
        self.setWindowTitle("Hasta Sahibi Paneli")
        self.setGeometry(100, 100, 800, 600)

        # UI'ı ayarla
        setup_ui(self)

        # Toolbar butonlarının işlevselliğini ayarla
        self.profile_action.triggered.connect(lambda: self.show_section("profile"))
        self.pets_action.triggered.connect(lambda: self.show_section("pets"))
        #self.appointments_action.triggered.connect(lambda: self.show_section("appointments"))

        # Verileri yükle
        self.load_profile()
        self.load_pets()
        #self.load_appointments()

        # Başlangıçta profil bölümünü göster
        self.show_section("profile")

    def show_section(self, section):
        """Seçilen bölümü gösterir, diğerlerini gizler"""
        # Tüm bölümleri gizle
        self.name_input.setVisible(False)
        self.email_input.setVisible(False)
        self.phone_input.setVisible(False)
        self.pets_table.setVisible(False)
        #self.appointments_table.setVisible(False)

        # Seçilen bölümü göster
        if section == "profile":
            self.name_input.setVisible(True)
            self.email_input.setVisible(True)
            self.phone_input.setVisible(True)
            self.profile_action.setChecked(True)
            self.pets_action.setChecked(False)
            #self.appointments_action.setChecked(False)
        elif section == "pets":
            self.pets_table.setVisible(True)
            self.profile_action.setChecked(False)
            self.pets_action.setChecked(True)
            #self.appointments_action.setChecked(False)

    def load_profile(self):
        """Kullanıcı profilini yükler ve arayüze yerleştir
        """
        profile_data = self.db.get_user_profile(self.user_data['id'])
        if profile_data:
            self.name_input.setText(profile_data['name'])
            self.email_input.setText(profile_data['email'])
            self.phone_input.setText(profile_data['phone'])
        else:
            print("Profil bilgileri yüklenemedi.")
            self.name_input.setText("")
            self.email_input.setText("")
            self.phone_input.setText("")
    def refresh_pets(self):

        """Kullanıcının hayvanlarını yükler ve tabloya yerleştirir"""
        pets = self.db.get_user_pets(self.user_data['id'])
        if pets:
            self.pets_table.setRowCount(len(pets))
            for i, pet in enumerate(pets):
                self.pets_table.setItem(i, 0, QTableWidgetItem(pet['name']))
                self.pets_table.setItem(i, 1, QTableWidgetItem(pet['type']))
                self.pets_table.setItem(i, 2, QTableWidgetItem(pet['breed']))
                self.pets_table.setItem(i, 3, QTableWidgetItem(str(pet['age'])))
        else:
            print("Hayvan bilgileri yüklenemedi.")
            self.pets_table.setRowCount(0)
            self.pets_table.setColumnCount(4)
            self.pets_table.setHorizontalHeaderLabels(["Ad", "Tür", "Cins", "Yaş"])

    def load_pets(self):
        """Kullanıcının hayvanlarını yükler ve tabloya yerleştirir"""
        pets = self.db.get_user_pets(self.user_data['id'])
        if pets:
            self.pets_table.setRowCount(len(pets))
            for i, pet in enumerate(pets):
                self.pets_table.setItem(i, 0, QTableWidgetItem(pet['name']))
                self.pets_table.setItem(i, 1, QTableWidgetItem(pet['type']))
                self.pets_table.setItem(i, 2, QTableWidgetItem(pet['breed']))
                self.pets_table.setItem(i, 3, QTableWidgetItem(str(pet['age'])))
        else:
            print("Hayvan bilgileri yüklenemedi.")
            self.pets_table.setRowCount(0)
            self.pets_table.setColumnCount(4)
            self.pets_table.setHorizontalHeaderLabels(["Ad", "Tür", "Cins", "Yaş"])


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

    def  add_new_pet(self):
        """Yeni bir hayvan eklemek için pencere açar"""
        from Windows.add_pet_window import AddPetWindow
        add_pet_window = AddPetWindow(self.db, self.user_data)
        add_pet_window.exec_()
        self.load_pets()
        # Hayvan eklendikten sonra tabloyu güncelle

    def add_appointment(self):
        """Yeni bir randevu almak için pencere açar"""
        from Windows.add_appointment_window import AddAppointmentWindow
        add_appointment_window = AddAppointmentWindow(self.db, self.user_data)
        add_appointment_window.exec_()
        self.load_appointments()
        # Randevu alındıktan sonra tabloyu güncelle
    def delete_pet(self):
        """Seçilen hayvanı siler"""
        selected_row = self.pets_table.currentRow()
        if selected_row >= 0:
            pet_name = self.pets_table.item(selected_row, 0).text()
            self.db.delete_pet(pet_name)
            self.load_pets()
        else:
            print("Silinecek hayvan seçilmedi.")

    def update_pet(self):
        """Seçilen hayvanı günceller"""
        selected_row = self.pets_table.currentRow()
        if selected_row >= 0:
            pet_name = self.pets_table.item(selected_row, 0).text()
            from Windows.update_pet_window import UpdatePetWindow
            update_pet_window = UpdatePetWindow(self.db, pet_name)
            update_pet_window.exec_()
            self.load_pets()
        else:
            print("Güncellenecek hayvan seçilmedi.")
