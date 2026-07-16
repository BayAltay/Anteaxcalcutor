# 🧮 Gizli Hesap Makinesi

Bir hesap makinesi + Şifreli not saklama uygulaması. Python Kivy ile yazılmıştır ve GitHub Actions ile otomatik olarak APK'ya derlenir.

## ✨ Özellikler

- ✅ **Tam Fonksiyonlu Hesap Makinesi**
  - Toplama, Çıkarma, Çarpma, Bölme
  - Ondalık sayı desteği
  - Hata kontrolü

- 🔐 **Şifreli Not Saklama**
  - Gizli notlar için şifre koruması (Varsayılan: 1234)
  - Not ekleme, düzenleme, silme
  - Otomatik tarih-saat kaydı
  - JSON dosyasında saklanır

- 📱 **Mobil Uyumlu**
  - Android 5.0+ desteklenir
  - APK olarak yüklenebilir
  - Çizgisi temiz UI

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Kivy 2.2+
- Buildozer (APK derlemesi için)

### Lokal Çalıştırma

```bash
# Depo klonla
git clone https://github.com/BayAltay/Anteaxcalcutor.git
cd Anteaxcalcutor

# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı çalıştır
python main.py
```

## 📦 APK Oluşturma

### GitHub Actions ile (Otomatik)

1. Kodunda değişiklik yap
2. `main` branch'e push et
3. GitHub Actions otomatik olarak derleyecek
4. APK dosyası Releases bölümünde bulunacak

### Lokal Derlemesi

```bash
pip install buildozer cython
buildozer android release
```

## 🔑 Gizli Notlara Erişim

**Varsayılan Şifre:** `1234`

Notlar menüsüne tıklayarak şifre girin ve notlarınız kaydolacak!

## 📝 Notlar

- Notlar `notes.json` dosyasında saklanır
- Her notu eklerken tarih-saat kaydı otomatik olur
- Notları düzenleyebilir veya silebilirsiniz

## 🛠️ Teknik Detaylar

- **Framework:** Kivy (Python UI Framework)
- **Storage:** JSON (Local)
- **Build Tool:** Buildozer
- **CI/CD:** GitHub Actions
- **Android Target:** API 31 (Android 12), Minimum API 21 (Android 5.0)

## 📄 Lisans

MIT License

## 👨‍💻 Geliştirici

BayAltay

---

**Son Yapı:** Bkz. [Releases](../../releases)
