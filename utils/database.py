import sqlite3
from pathlib import Path
import hashlib
import uuid


class Database:
    def __init__(self):
        self.db_file = Path("veteriner.db")
        self.create_tables()
        self.migrate_database()
        self.create_default_admin()

    def create_tables(self):
        """Veritabanı tablolarını oluşturur"""
        conn = sqlite3.connect(str(self.db_file))
        cursor = conn.cursor()

        # Kullanıcılar tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kullanicilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT UNIQUE NOT NULL,
                sifre_hash TEXT NOT NULL,
                tuz TEXT NOT NULL,
                rol TEXT NOT NULL,
                ad_soyad TEXT NOT NULL,
                email TEXT,
                son_giris DATETIME
            )
        ''')

        # Yetkiler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS yetkiler (
                rol TEXT PRIMARY KEY,
                hasta_ekle BOOLEAN,
                hasta_duzenle BOOLEAN,
                hasta_sil BOOLEAN,
                rapor_goruntule BOOLEAN,
                kullanici_yonet BOOLEAN
            )
        ''')

        # Hastalar tablosu
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS hastalar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hayvan_adi TEXT NOT NULL,
                    sahip_adi TEXT NOT NULL,
                    tur TEXT NOT NULL,
                    cins TEXT,
                    cinsiyet TEXT NOT NULL,
                    yas INTEGER NOT NULL,
                    durum TEXT NOT NULL,
                    ilerleme INTEGER NOT NULL,
                    sikayet TEXT,
                    aciklama TEXT,
                    ilaclar TEXT,
                    ekleyen_id INTEGER,
                    ekleme_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ekleyen_id) REFERENCES kullanicilar(id)
                )
            ''')

        # Varsayılan yetkileri ekle
        cursor.execute('''INSERT OR IGNORE INTO yetkiler VALUES 
            ('admin', 1, 1, 1, 1, 1),
            ('doktor', 1, 1, 0, 1, 0),
            ('asistan', 0, 0, 0, 1, 0)
        ''')

        conn.commit()
        conn.close()

    def create_default_admin(self):
        """Varsayılan admin kullanıcısını oluşturur"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            # Önce mevcut admin kullanıcısını sil
            cursor.execute('DELETE FROM kullanicilar WHERE kullanici_adi = ?', ('admin',))
            conn.commit()

            # Yeni admin kullanıcısını oluştur
            tuz = uuid.uuid4().hex
            sifre = "123"
            sifre_hash = hashlib.sha256((sifre + tuz).encode()).hexdigest()

            cursor.execute('''
                INSERT INTO kullanicilar (kullanici_adi, sifre_hash, tuz, rol, ad_soyad, email)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('123', sifre_hash, tuz, 'admin', 'Sistem Yöneticisi', 'admin@veteriner.com'))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Admin oluşturma hatası: {e}")

    def login(self, kullanici_adi, sifre):
        """Kullanıcı girişi yapar"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('SELECT id, sifre_hash, tuz, rol FROM kullanicilar WHERE kullanici_adi = ?', (kullanici_adi,))
            user = cursor.fetchone()

            if user:
                user_id, stored_hash, tuz, rol = user
                sifre_hash = hashlib.sha256((sifre + tuz).encode()).hexdigest()

                if sifre_hash == stored_hash:
                    # Son giriş tarihini güncelle
                    cursor.execute('UPDATE kullanicilar SET son_giris = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
                    conn.commit()

                    # Yetkileri al
                    cursor.execute('SELECT * FROM yetkiler WHERE rol = ?', (rol,))
                    yetkiler = cursor.fetchone()

                    conn.close()
                    return {'success': True, 'user_id': user_id, 'rol': rol, 'yetkiler': {'hasta_ekle': yetkiler[1], 'hasta_duzenle': yetkiler[2], 'hasta_sil': yetkiler[3], 'rapor_goruntule': yetkiler[4], 'kullanici_yonet': yetkiler[5]}}

            conn.close()
            return {'success': False, 'error': 'Geçersiz kullanıcı adı veya şifre'}

        except Exception as e:
            print(f"Giriş hatası: {e}")
            return {'success': False, 'error': 'Giriş işlemi sırasında bir hata oluştu'}

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

    def add_patient(self, data):
        """Yeni hasta kaydı ekler"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute('''
                        INSERT INTO hastalar (
                            hayvan_adi, sahip_adi, tur, cinsiyet, cins, yas, 
                            durum, ilerleme, sikayet, aciklama, ilaclar, ekleyen_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (data['hayvan_adi'], data['sahip_adi'], data['tur'], data['cinsiyet'], data['cins'], data['yas'], data['durum'], data['ilerleme'], data.get('sikayet', ''),  # Fix: Use get() with default value
                          data.get('aciklama', ''), data.get('ilaclar', ''), data.get('ekleyen_id')))

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
                        SELECT id, hayvan_adi, sahip_adi, tur, cins, cinsiyet, 
                               yas, durum, ilerleme, sikayet, aciklama, ilaclar, ekleme_tarihi 
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

    def update_patient(self, patient_id, column, value):
        """Hasta bilgilerini günceller"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()

            cursor.execute(f'UPDATE hastalar SET {column} = ? WHERE id = ?', (value, patient_id))

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
                        SET hayvan_adi=?, sahip_adi=?, tur=?, cinsiyet=?, cins=?, yas=?, 
                            durum=?, ilerleme=?, sikayet=?, aciklama=?, ilaclar=?
                        WHERE id=?
                    ''', (data['hayvan_adi'], data['sahip_adi'], data['tur'], data['cinsiyet'], data['cins'], data['yas'], data['durum'], data['ilerleme'], data['sikayet'], data['aciklama'], data['ilaclar'], record_id))

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

            # 'cins' sütunu yoksa ekle
            if 'sikayet' not in columns:
                cursor.execute('ALTER TABLE hastalar ADD COLUMN sikayet TEXT')
                print("'sikayet' sütunu eklendi")

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
                SELECT id, hayvan_adi, sahip_adi, tur, cins, cinsiyet,
                       yas, durum, ilerleme, sikayet, aciklama, ilaclar, 
                       ekleme_tarihi
                FROM hastalar
                WHERE durum = 'Muayene Bekliyor'
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

            # Durumu güncelle
            cursor.execute('''
                UPDATE hastalar 
                SET durum = 'Teşhis Konuldu'
                WHERE id = ?
            ''', (hasta_id,))

            # Hasta bilgilerini getir
            cursor.execute('''
                SELECT hayvan_adi, sahip_adi, tur, cins, cinsiyet, yas,
                       sikayet, aciklama, ilaclar, durum, ilerleme
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