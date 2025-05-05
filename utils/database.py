import sqlite3
import hashlib
import uuid


class Database:
    def __init__(self):
        self.db_file = "veteriner.db"
        self.create_tables()
        self.migrate_database()
        self.create_default_admin()

    def create_tables(self):
        """Veritabanı tablolarını oluşturur"""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()

        # Kullanıcılar tablosu
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS kullanicilar
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           kullanici_adi
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           sifre_hash
                           TEXT
                           NOT
                           NULL,
                           tuz
                           TEXT
                           NOT
                           NULL,
                           rol
                           TEXT
                           NOT
                           NULL,
                           ad_soyad
                           TEXT
                           NOT
                           NULL,
                           email
                           TEXT,
                           son_giris
                           DATETIME
                       )
                       ''')

        # Yetkiler tablosu
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS yetkiler
                       (
                           rol
                           TEXT
                           PRIMARY
                           KEY,
                           hasta_ekle
                           BOOLEAN,
                           hasta_duzenle
                           BOOLEAN,
                           hasta_sil
                           BOOLEAN,
                           rapor_goruntule
                           BOOLEAN,
                           kullanici_yonet
                           BOOLEAN
                       )
                       ''')

        # Hastalar tablosu
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS hastalar
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           hayvan_adi
                           TEXT
                           NOT
                           NULL,
                           sahip_adi
                           TEXT
                           NOT
                           NULL,
                           tur
                           TEXT
                           NOT
                           NULL,
                           cins
                           TEXT,
                           cinsiyet
                           TEXT
                           NOT
                           NULL,
                           yas
                           INTEGER
                           NOT
                           NULL,
                           durum
                           TEXT
                           NOT
                           NULL,
                           ilerleme
                           INTEGER
                           NOT
                           NULL,
                           sikayet
                           TEXT,
                           aciklama
                           TEXT,
                           ilaclar
                           TEXT,
                           ekleyen_id
                           INTEGER,
                           ekleme_tarihi
                           DATETIME
                           DEFAULT
                           CURRENT_TIMESTAMP,
                           tarih
                           TEXT
                           DEFAULT
                           NULL,
                           saat
                           TEXT
                           DEFAULT
                           NULL,
                           FOREIGN
                           KEY
                       (
                           ekleyen_id
                       ) REFERENCES kullanicilar
                       (
                           id
                       )
                           )
                       ''')

        # Varsayılan yetkileri ekle
        cursor.execute('''INSERT
        OR IGNORE INTO yetkiler VALUES 
            ('admin', 1, 1, 1, 1, 1),
            ('doktor', 1, 1, 1, 1, 0),
            ('asistan', 1, 0, 0, 1, 0),
            ('hasta_sahibi', 0, 0, 0, 0, 0)
                       ''')

        # Kullanıcı petler tablosu
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS pets
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           hayvan_adi
                           TEXT
                           NOT
                           NULL,
                           tur
                           TEXT
                           NOT
                           NULL,
                           cins
                           TEXT,
                           cinsiyet
                           TEXT
                           NOT
                           NULL,
                           yas
                           INTEGER
                           NOT
                           NULL,
                           ekleyen_id
                           INTEGER,
                           FOREIGN
                           KEY
                       (
                           ekleyen_id
                       ) REFERENCES kullanicilar
                       (
                           id
                       )
                           )
                       ''')

        conn.commit()
        conn.close()

    def create_default_admin(self):
        """Create default admin user if not exists"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            # Check if admin already exists
            cursor.execute('SELECT COUNT(*) FROM kullanicilar WHERE kullanici_adi = ?', ('admin',))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return  # Admin already exists, don't recreate

            # Create admin user
            tuz = uuid.uuid4().hex
            sifre = "admin"
            sifre_hash = hashlib.sha256((sifre + tuz).encode()).hexdigest()

            cursor.execute('''
                           INSERT INTO kullanicilar (kullanici_adi, sifre_hash, tuz, rol, ad_soyad, email)
                           VALUES (?, ?, ?, ?, ?, ?)
                           ''', ('admin', sifre_hash, tuz, 'admin', 'Sistem Yöneticisi', 'admin@veteriner.com'))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Admin oluşturma hatası: {e}")

    def login(self, kullanici_adi, sifre, role_type=None):
        """User login"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            # Role specific query if role_type is provided
            if role_type:
                query = 'SELECT id, sifre_hash, tuz, rol FROM kullanicilar WHERE kullanici_adi = ? AND rol = ?'
                cursor.execute(query, (kullanici_adi, role_type))
            else:
                cursor.execute('SELECT id, sifre_hash, tuz, rol FROM kullanicilar WHERE kullanici_adi = ?', (kullanici_adi,))

            user = cursor.fetchone()

            if user:
                user_id, stored_hash, tuz, rol = user
                sifre_hash = hashlib.sha256((sifre + tuz).encode()).hexdigest()

                if sifre_hash == stored_hash:
                    cursor.execute('UPDATE kullanicilar SET son_giris = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
                    conn.commit()

                    # Get permissions for the role
                    cursor.execute('SELECT * FROM yetkiler WHERE rol = ?', (rol,))
                    yetkiler = cursor.fetchone()

                    # If permissions not found, use default no-permissions
                    if not yetkiler:
                        yetkiler = (rol, 0, 0, 0, 0, 0)

                    conn.close()
                    return {'success': True, 'user_id': user_id, 'rol': rol, 'yetkiler': {'hasta_ekle': yetkiler[1], 'hasta_duzenle': yetkiler[2], 'hasta_sil': yetkiler[3], 'rapor_goruntule': yetkiler[4], 'kullanici_yonet': yetkiler[5]},
                            'id': user_id  # 'id' anahtarını ekle
                            }

            conn.close()
            return {'success': False, 'error': 'Invalid username or password'}

        except Exception as e:
            print(f"Login error: {e}")
            return {'success': False, 'error': f'An error occurred during login: {str(e)}'}

    def add_user(self, data, admin_id):
        """Yeni kullanıcı ekler"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            # Admin yetkisi kontrol et
            cursor.execute('SELECT rol FROM kullanicilar WHERE id = ?', (admin_id,))
            admin_rol = cursor.fetchone()

            if admin_rol and admin_rol[0] == 'admin':
                tuz = uuid.uuid4().hex
                sifre_hash = hashlib.sha256((data['sifre'] + tuz).encode()).hexdigest()

                cursor.execute('''
                               INSERT INTO kullanicilar (kullanici_adi, sifre_hash, tuz, rol, ad_soyad, email)
                               VALUES (?, ?, ?, ?, ?, ?)
                               ''', (data['kullanici_adi'], sifre_hash, tuz, data['rol'], data['ad_soyad'], data.get('email', '')))

                conn.commit()
                conn.close()
                return True

            conn.close()
            return False

        except Exception as e:
            print(f"Kullanıcı ekleme hatası: {e}")
            return False

    def update_user_profile(self, user_id, name, tc, email, phone, username, new_password):
        """Kullanıcı profilini günceller"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            # Kullanıcı bilgilerini güncelle
            cursor.execute('''
                           UPDATE kullanicilar
                           SET ad_soyad      = ?,
                               tc_kimlik     = ?,
                               email         = ?,
                               telefon       = ?,
                               kullanici_adi = ?
                           WHERE id = ?
                           ''', (name, tc, email, phone, username, user_id))

            # Şifreyi güncelle
            if new_password:
                tuz = uuid.uuid4().hex
                sifre_hash = hashlib.sha256((new_password + tuz).encode()).hexdigest()
                cursor.execute('''UPDATE kullanicilar
                                  SET sifre_hash = ?,
                                      tuz        = ?
                                  WHERE id = ?''', (sifre_hash, tuz, user_id))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Kullanıcı güncelleme hatası: {e}")
            return False

    def add_patient(self, data):
        """Yeni hasta kaydı ekler"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            # Eksik alanları kontrol et ve varsayılan değerler ata
            if 'durum' not in data:
                data['durum'] = 'Muayene Bekliyor'
            if 'ilerleme' not in data:
                data['ilerleme'] = 0

            cursor.execute('''
                           INSERT INTO hastalar (hayvan_adi, sahip_adi, tur, cinsiyet, cins, yas,
                                                 durum, ilerleme, sikayet, aciklama, ilaclar, ekleyen_id, tarih, saat)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ''', (data['hayvan_adi'], data['sahip_adi'], data['tur'], data['cinsiyet'], data.get('cins', ''),  # Boş değer yerine varsayılan değer kullan
                                 data['yas'], data['durum'], data['ilerleme'], data.get('sikayet', ''),  # Boş değer yerine varsayılan değer kullan
                                 data.get('aciklama', ''),  # Boş değer yerine varsayılan değer kullan
                                 data.get('ilaclar', ''),  # Boş değer yerine varsayılan değer kullan
                                 data.get('ekleyen_id', None),  # Null değer yerine None kullan
                                 data.get('tarih', None),  # Null değer yerine None kullan
                                 data.get('saat', None)))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Veritabanı hatası: {e}")
            return False

    def get_all_patients(self):
        """Tüm hastaları getirir"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT id,
                                  hayvan_adi,
                                  sahip_adi,
                                  tur,
                                  cins,
                                  cinsiyet,
                                  yas,
                                  durum,
                                  ilerleme,
                                  sikayet,
                                  aciklama,
                                  ilaclar,
                                  ekleme_tarihi
                           FROM hastalar
                           ORDER BY id DESC
                           ''')

            records = cursor.fetchall()
            conn.close()
            return records

        except Exception as e:
            print(f"Veritabanı hatası: {e}")
            return []

    def delete_patient(self, patient_id):
        """Hasta kaydını siler"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('DELETE FROM hastalar WHERE id = ?', (patient_id,))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Veritabanı hatası: {e}")
            return False

    def get_statistics(self):
        """İstatistikleri hesaplar"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            # Toplam hasta sayısı
            cursor.execute('SELECT COUNT(*) FROM hastalar')
            total = cursor.fetchone()[0]

            # Tedavi başarı oranı (ilerleme > 80 olanlar)
            cursor.execute('SELECT COUNT(*) FROM hastalar WHERE ilerleme > 80')
            success = cursor.fetchone()[0]

            success_rate = (success / total * 100) if total > 0 else 0

            conn.close()
            return {'total': total, 'success_rate': success_rate}

        except Exception as e:
            print(f"Veritabanı hatası: {e}")
            return {'total': 0, 'success_rate': 0}

    def update_patient_full(self, record_id, data):
        """Hasta kaydını tüm alanlarıyla günceller"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           UPDATE hastalar
                           SET hayvan_adi=?,
                               sahip_adi=?,
                               tur=?,
                               cinsiyet=?,
                               cins=?,
                               yas=?,
                               durum=?,
                               ilerleme=?,
                               sikayet=?,
                               aciklama=?,
                               ilaclar=?,
                               tarih=?,
                               saat=?
                           WHERE id = ?
                           ''',
                           (data['hayvan_adi'], data['sahip_adi'], data['tur'], data['cinsiyet'], data['cins'], data['yas'], data['durum'], data['ilerleme'], data['sikayet'], data['aciklama'], data['ilaclar'], data['tarih'], data['saat'], record_id))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Güncelleme hatası: {e}")
            return False

    def migrate_database(self):
        """Veritabanı şemasını günceller"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            # Mevcut sütunları kontrol et
            cursor.execute("PRAGMA table_info(hastalar)")
            columns = [column[1] for column in cursor.fetchall()]

            # 'sikayet' sütunu yoksa ekle
            if 'tarih' not in columns:
                cursor.execute('ALTER TABLE hastalar ADD COLUMN tarih TEXT DEFAULT NULL')
                print("'tarih' sütunu eklendi")
            if 'saat' not in columns:
                cursor.execute('ALTER TABLE hastalar ADD COLUMN saat TEXT DEFAULT NULL')
                print("'saat' sütunu eklendi")

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Migrasyon hatası: {e}")

    def get_waiting_patients(self):
        """Muayene bekleyen hastaları getirir"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT id,
                                  hayvan_adi,
                                  sahip_adi,
                                  tur,
                                  cins,
                                  cinsiyet,
                                  yas,
                                  durum,
                                  ilerleme,
                                  sikayet,
                                  aciklama,
                                  ilaclar,
                                  ekleme_tarihi
                           FROM hastalar
                           WHERE durum IN ('Muayene Bekliyor', 'Acil Durum')
                           ORDER BY ekleme_tarihi DESC
                           ''')

            records = cursor.fetchall()
            conn.close()
            return records

        except Exception as e:
            print(f"Veritabanı hatası: {e}")
            return []

    def update_patient_status(self, patient_id, new_status):
        """Hasta durumunu günceller"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           UPDATE hastalar
                           SET durum = ?
                           WHERE id = ?
                           ''', (new_status, patient_id))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Veritabanı hatası: {e}")
            return False

    def muayeneye_al(self, hasta_id):
        """Hastayı muayeneye alır ve bilgilerini getirir"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            # Hasta bilgilerini getir
            cursor.execute('''
                           SELECT hayvan_adi,
                                  sahip_adi,
                                  tur,
                                  cins,
                                  cinsiyet,
                                  yas,
                                  sikayet,
                                  aciklama,
                                  ilaclar,
                                  durum,
                                  ilerleme
                           FROM hastalar
                           WHERE id = ?
                           ''', (hasta_id,))
            hasta = cursor.fetchone()

            conn.commit()
            conn.close()
            return hasta if hasta else None

        except Exception as e:
            print(f"Muayeneye alma hatası: {e}")
            return None

    def register_user(self, data):
        """Yeni kullanıcı kaydeder"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            # Kullanıcı adı kontrolü
            cursor.execute('SELECT COUNT(*) FROM kullanicilar WHERE kullanici_adi = ?', (data['kullanici_adi'],))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return False

            # Şifre hashleme
            tuz = uuid.uuid4().hex
            sifre_hash = hashlib.sha256((data['sifre'] + tuz).encode()).hexdigest()

            # Gerekli sütunları kontrol et
            cursor.execute("PRAGMA table_info(kullanicilar)")
            columns = [column[1] for column in cursor.fetchall()]

            # Gerekli sütunları ekle
            if 'tc_kimlik' not in columns:
                cursor.execute('ALTER TABLE kullanicilar ADD COLUMN tc_kimlik TEXT')
            if 'telefon' not in columns:
                cursor.execute('ALTER TABLE kullanicilar ADD COLUMN telefon TEXT')

            # SQL sorgusunu hazırla
            cursor.execute('''
                           INSERT INTO kullanicilar (kullanici_adi, sifre_hash, tuz, rol, ad_soyad, email, tc_kimlik, telefon)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                           ''', (data['kullanici_adi'], sifre_hash, tuz, data.get('rol', 'hasta_sahibi'),  # Varsayılan rol
                                 data['ad_soyad'], data.get('email', ''),  # Email yoksa boş string
                                 data.get('tc_kimlik', ''),  # TC kimlik yoksa boş string
                                 data.get('telefon', '')  # Telefon yoksa boş string
                                 ))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Kullanıcı kayıt hatası: {e}")
            return False

    def get_user_pets(self, user_id):
        """Belirli bir kullanıcının hayvanlarını getirir"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT hayvan_adi AS name, tur AS type, cins AS breed, yas AS age
                           FROM hastalar
                           WHERE ekleyen_id = ?
                           ''', (user_id,))

            pets = cursor.fetchall()
            conn.close()
            return [{'name': pet[0], 'type': pet[1], 'breed': pet[2], 'age': pet[3]} for pet in pets]

        except Exception as e:
            print(f"Hayvanları getirme hatası: {e}")
            return []

    def get_user_profile(self, user_id):
        """Belirli bir kullanıcının profil bilgilerini getirir"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT ad_soyad, tc_kimlik, email, telefon, kullanici_adi, sifre_hash, tuz
                           FROM kullanicilar
                           WHERE id = ?
                           ''', (user_id,))

            profile = cursor.fetchone()
            conn.close()

            # Profil bilgilerini döndür
            return {'id': user_id, 'name': profile[0], 'tc': profile[1], 'email': profile[2], 'phone': profile[3], 'username': profile[4], 'hash': profile[5], 'tuz': profile[6]

                    } if profile else None

        except Exception as e:
            print(f"Profil bilgilerini getirme hatası: {e}")
            return None

    def add_pet(self, user_id, pet_data):
        """Kullanıcıya yeni hayvan ekler"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           INSERT INTO pets (hayvan_adi, tur, cins, cinsiyet, yas, ekleyen_id)
                           VALUES (?, ?, ?, ?, ?, ?)
                           ''', (pet_data['hayvan_adi'], pet_data['tur'], pet_data['cins'], pet_data['cinsiyet'], pet_data['yas'], user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Hayvan ekleme hatası: {e}")
            return False

    def get_pets(self, user_id):
        """Kullanıcıya ait hayvanları getirir"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT id, hayvan_adi, tur, cins, cinsiyet, yas
                           FROM pets
                           WHERE ekleyen_id = ?
                           ''', (user_id,))

            pets = cursor.fetchall()
            conn.close()
            return pets
        except Exception as e:
            print(f"Hayvanları getirme hatası: {e}")
            return None

    def get_pet(self, pet_id):
        """Hayvan kaydını getirir"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT hayvan_adi, tur, cins, cinsiyet, yas, id
                           FROM pets
                           WHERE id = ?
                           ''', (pet_id,))

            pet = cursor.fetchone()
            conn.close()
            return pet

        except Exception as e:
            print(f"Hayvan bilgilerini getirme hatası: {e}")
            return None

    def delete_pet(self, pet_id):
        """Hayvan kaydını siler"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('DELETE FROM pets WHERE id = ?', (pet_id,))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Hayvan silme hatası: {e}")
            return False

    def update_pet(self, pet_id, data):
        """Hayvan kaydını günceller"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           UPDATE pets
                           SET hayvan_adi = ?,
                               tur        = ?,
                               cins       = ?,
                               cinsiyet   = ?,
                               yas        = ?
                           WHERE id = ?
                           ''', (data['hayvan_adi'], data['tur'], data['cins'], data['cinsiyet'], data['yas'], pet_id))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Hayvan güncelleme hatası: {e}")
            return False

    def add_appointment(self, appointment_data):
        """Randevu ekler"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           INSERT INTO randevular (pet_id, tarih, saat, durum)
                           VALUES (?, ?, ?, ?)
                           ''', (appointment_data['pet_id'], appointment_data['tarih'], appointment_data['saat'], 'Bekliyor'))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Randevu ekleme hatası: {e}")
            return False

    def get_appointments(self, pet_id):
        """Hayvana ait randevuları getirir"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT id, pet_id, tarih, saat, durum
                           FROM randevular
                           WHERE pet_id = ?
                           ''', (pet_id,))

            appointments = cursor.fetchall()
            conn.close()
            return appointments
        except Exception as e:
            print(f"Randevu bilgilerini getirme hatası: {e}")
            return None

    def delete_appointment(self, appointment_id):
        """Randevuyu siler"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('DELETE FROM randevular WHERE id = ?', (appointment_id,))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Randevu silme hatası: {e}")
            return False

    def get_patient_id(self,pet_name, date, time):
        """Hasta ID'sini alır"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT id
                           FROM hastalar
                           WHERE hayvan_adi = ? AND tarih = ? AND saat = ?
                           ''', (pet_name, date, time))

            patient_id = cursor.fetchone()
            conn.close()
            return patient_id[0] if patient_id else None

        except Exception as e:
            print(f"Hasta ID'sini alma hatası: {e}")
            return None
