import sqlite3
import bcrypt
import datetime
import matplotlib.pyplot as plt

# Veritabanı bağlantısı
def veritabani_baglantisi():
    conn = sqlite3.connect('finansal_veriler.db')
    return conn

# Kullanıcı tablosu ve harcama, gelir tablolarının oluşturulması
def tablo_olustur():
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT NOT NULL,
            sifre TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS harcamalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_id INTEGER,
            tarih TEXT,
            kategori TEXT,
            miktar REAL,
            FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gelirler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_id INTEGER,
            tarih TEXT,
            kategori TEXT,
            miktar REAL,
            FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id)
        )
    """)
    conn.commit()
    conn.close()

# Kullanıcı kaydı
def kullanici_kaydet():
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    kullanici_adi = input("Kullanıcı adı: ")
    sifre = input("Şifre: ")
    sifre_hash = bcrypt.hashpw(sifre.encode('utf-8'), bcrypt.gensalt())

    cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (kullanici_adi, sifre_hash))
    conn.commit()
    conn.close()
    print("Kullanıcı kaydedildi!")

# Kullanıcı girişi
def kullanici_giris():
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    kullanici_adi = input("Kullanıcı adı: ")
    sifre = input("Şifre: ")

    cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi = ?", (kullanici_adi,))
    kullanici = cursor.fetchone()

    if kullanici and bcrypt.checkpw(sifre.encode('utf-8'), kullanici[2]):
        print("Giriş başarılı!")
        return kullanici[0]  # Kullanıcı ID'sini döndür
    else:
        print("Kullanıcı adı veya şifre yanlış!")
        return None

    conn.close()

# Harcama kaydetme
def harcama_kaydet(kullanici_id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    print("Harcama Türleri: 1. Maaş 2. Komisyon 3. Kiralama 4. Yiyecek 5. Ulaşım 6. Diğer")
    harcama_turu = input("Harcama türünü seçin (1-6): ")
    harcama_turu_dict = {
        "1": "Maaş",
        "2": "Komisyon",
        "3": "Kiralama",
        "4": "Yiyecek",
        "5": "Ulaşım",
        "6": "Diğer"
    }

    miktar = float(input("Harcama miktarı: "))
    tarih = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO harcamalar (kullanici_id, tarih, kategori, miktar) VALUES (?, ?, ?, ?)",
                   (kullanici_id, tarih, harcama_turu_dict[harcama_turu], miktar))
    conn.commit()
    conn.close()

    print("Harcama kaydedildi!")

# Gelir kaydetme
def gelir_kaydet(kullanici_id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    print("Gelir Türleri: 1. Maaş 2. Komisyon 3. Ekstra Gelir 4. Yatırım Geliri 5. Diğer")
    gelir_turu = input("Gelir türünü seçin (1-5): ")
    gelir_turu_dict = {
        "1": "Maaş",
        "2": "Komisyon",
        "3": "Ekstra Gelir",
        "4": "Yatırım Geliri",
        "5": "Diğer"
    }

    miktar = float(input("Gelir miktarı: "))
    tarih = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO gelirler (kullanici_id, tarih, kategori, miktar) VALUES (?, ?, ?, ?)",
                   (kullanici_id, tarih, gelir_turu_dict[gelir_turu], miktar))
    conn.commit()
    conn.close()

    print("Gelir kaydedildi!")

# Toplam gelir ve gider
def toplam_gelir_ve_gider(kullanici_id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(miktar) FROM gelirler WHERE kullanici_id = ?", (kullanici_id,))
    toplam_gelir = cursor.fetchone()[0] or 0  # Eğer gelir yoksa 0 döner

    cursor.execute("SELECT SUM(miktar) FROM harcamalar WHERE kullanici_id = ?", (kullanici_id,))
    toplam_gider = cursor.fetchone()[0] or 0  # Eğer gider yoksa 0 döner

    print(f"Toplam Gelir: {toplam_gelir}")
    print(f"Toplam Gider: {toplam_gider}")
    print(f"Şimdiki Para: {toplam_gelir - toplam_gider}")
    conn.close()

# En yüksek gider
def en_yuksek_gider(kullanici_id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    cursor.execute("SELECT kategori, MAX(miktar) FROM harcamalar WHERE kullanici_id = ?", (kullanici_id,))
    max_gider = cursor.fetchone()
    print(f"En Yüksek Gider Kategorisi: {max_gider[0]} - {max_gider[1]} TL")
    conn.close()

# Yıl ve aylık harcamalar
def yil_ve_aylik_harcamalar(kullanici_id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    yil = input("Yıl girin (örneğin 2024): ")
    ay = input("Ay girin (1-12): ")

    cursor.execute("""
        SELECT kategori, SUM(miktar) FROM harcamalar
        WHERE kullanici_id = ? AND strftime('%Y', tarih) = ? AND strftime('%m', tarih) = ?
        GROUP BY kategori
    """, (kullanici_id, yil, ay))

    harcamalar = cursor.fetchall()
    print(f"{yil} yılı {ay}. ay için harcamalar:")
    for kategori, miktar in harcamalar:
        print(f"{kategori}: {miktar} TL")
    conn.close()

# Bütçe limiti
def butce_limiti(kullanici_id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    limit = float(input("Bütçe limiti belirleyin: "))

    cursor.execute("SELECT SUM(miktar) FROM harcamalar WHERE kullanici_id = ?", (kullanici_id,))
    toplam_harcama = cursor.fetchone()[0] or 0

    if toplam_harcama > limit:
        print(f"Uyarı! Toplam harcama {toplam_harcama} TL, belirlediğiniz limit {limit} TL'yi aştı.")
    else:
        print(f"Toplam harcama {toplam_harcama} TL, bütçe limiti içerisinde.")
    conn.close()

# Günlük ve haftalık raporlar
def gunluk_ve_haftalik_raporlar(kullanici_id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    bugun = datetime.datetime.now()
    bir_hafta_once = bugun - datetime.timedelta(weeks=1)
    bugun_str = bugun.strftime("%Y-%m-%d")
    bir_hafta_once_str = bir_hafta_once.strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT SUM(miktar) FROM harcamalar WHERE kullanici_id = ? AND tarih BETWEEN ? AND ?
    """, (kullanici_id, bir_hafta_once_str, bugun_str))
    haftalik_gider = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(miktar) FROM gelirler WHERE kullanici_id = ? AND tarih BETWEEN ? AND ?
    """, (kullanici_id, bir_hafta_once_str, bugun_str))
    haftalik_gelir = cursor.fetchone()[0] or 0

    print(f"Haftalık Gider: {haftalik_gider} TL")
    print(f"Haftalık Gelir: {haftalik_gelir} TL")
    conn.close()

def en_fazla_harcama_yapilan_kategori(kullanici_id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT kategori, SUM(miktar) as toplam_miktar
        FROM harcamalar
        WHERE kullanici_id = ?
        GROUP BY kategori
        ORDER BY toplam_miktar DESC
        LIMIT 1
    """, (kullanici_id,))
    
    sonuc = cursor.fetchone()
    if sonuc:
        print(f"En fazla harcama yapılan kategori: {sonuc[0]} - Toplam: {sonuc[1]}")
    else:
        print("Hiç harcama kaydı bulunamadı.")
    
    conn.close()

# İşlemleri Listele
def islemleri_listele(kullanici_id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM harcamalar WHERE kullanici_id = ?", (kullanici_id,))
    harcamalar = cursor.fetchall()
    print("Harcamalar:")
    for harcama in harcamalar:
        print(harcama)

    cursor.execute("SELECT * FROM gelirler WHERE kullanici_id = ?", (kullanici_id,))
    gelirler = cursor.fetchall()
    print("\nGelirler:")
    for gelir in gelirler:
        print(gelir)

    conn.close()

# Ana Menü
def ana_menu(kullanici_id):
    while True:
        print("\n1. Harcama Kaydet")
        print("2. Gelir Kaydet")
        print("3. İşlemleri Listele")
        print("4. En Fazla Harcama Yapılan Kategori")
        print("5. Toplam Gelir ve Gider")
        print("6. En Yüksek Gider")
        print("7. Yıl ve Aylık Harcamalar")
        print("0. Çıkış")
        secim = input("Seçiminizi yapın: ")

        if secim == "1":
            harcama_kaydet(kullanici_id)
        elif secim == "2":
            gelir_kaydet(kullanici_id)
        elif secim == "3":
            islemleri_listele(kullanici_id)
        elif secim == "4":
            en_fazla_harcama_yapilan_kategori(kullanici_id)
        elif secim == "5":
            toplam_gelir_ve_gider(kullanici_id)
        elif secim == "6":
            en_yuksek_gider(kullanici_id)
        elif secim == "7":
            yil_ve_aylik_harcamalar(kullanici_id)
        elif secim == "0":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim. Tekrar deneyin.")

def ascii_sanati():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    art = """
______ _                            
|  ___(_)                           
| |_   _ _ __   __ _ _ __   ___ ___ 
|  _| | | '_ \\ / _` | '_ \\ / __/ _ \\
| |   | | | | | (_| | | | | (_|  __/
\\_|   |_|_| |_|\__,_|_| |_|\___\___|
                                    
             # Bütçe Yönetim Sistemi
                 # Developed by Uwpear
"""
    print(art)

# programın başlangıcı buradan başlar ⬇︎
def main():
    ascii_sanati()
    tablo_olustur()
    print("Hoş geldiniz!")
    while True:
        print("\n1. Kayıt Ol")
        print("2. Giriş Yap")
        print("0. Çıkış")

        secim = input("Bir seçenek girin: ")

        if secim == "1":
            kullanici_kaydet()
        elif secim == "2":
            kullanici_id = kullanici_giris()
            if kullanici_id:
                ana_menu(kullanici_id)
        elif secim == "0":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçenek!")

if __name__ == "__main__":
    main()
