# Hes(y)ap

Bu proje ile kişisel finans yönetimi yapılabilir, kullanıcılar gelir ve giderlerini kaydedebilir, harcamalarını kategorilere göre takip edebilir ve finansal durumlarını analiz edebilirler!

## Özellikler

- Kullanıcı kaydı ve girişi
- Gelir ve gider kaydetme
- Harcamaları ve gelirleri listeleme
- En fazla harcama yapılan kategoriyi gösterme
- Toplam gelir ve gider hesaplama
- En yüksek gideri gösterme
- Yıl ve aylık harcamaları gösterme
- Bütçe limiti belirleme ve kontrol etme
- Günlük ve haftalık raporlar

- Kullanıcı bilgiler bcrypt kütüphanesi ile şifrelenir!
## Kurulum

1. Bu projeyi klonlayın veya indirin:
    ```bash
    git clone https://github.com/kullanici_adi/hesyap.git
    cd hesyap
    ```

2. Gerekli Python paketlerini yükleyin:
    ```bash
    pip3 install -r requirements.txt
    ```

3. Veritabanını oluşturun:
    ```bash
    python3 finance.py
    ```

## Kullanım

1. Programı çalıştırın:
    ```bash
    python3 finance.py
    ```

2. Ana menüden bir seçenek seçin:
    - `1`: Kayıt Ol
    - `2`: Giriş Yap
    - `0`: Çıkış

3. Giriş yaptıktan sonra, aşağıdaki işlemleri gerçekleştirebilirsiniz:
    - `1`: Harcama Kaydet
    - `2`: Gelir Kaydet
    - `3`: İşlemleri Listele
    - `4`: En Fazla Harcama Yapılan Kategori
    - `5`: Toplam Gelir ve Gider
    - `6`: En Yüksek Gider
    - `7`: Yıl ve Aylık Harcamalar
    - `0`: Çıkış

## Gereksinimler

- Python 3.x
- sqlite3 modülü
- bcrypt modülü
- matplotlib modülü

## Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya bir issue açın.

## İletişim

Herhangi bir sorunuz veya geri bildiriminiz varsa, lütfen [mutedeveloper@tuta.io](mailto:mutedeveloper@tuta.io) adresinden bizimle iletişime geçin.

---

**Not:** Bu proje, kişisel finans yönetimi için basit bir uygulama olarak geliştirilmiştir ve ticari kullanım için uygun olmayabilir. Çok da ciddiye almayalım.
