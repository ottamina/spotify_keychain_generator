# 🎵 Spotify Keychain 3D Model Generator

Spotify şarkı, albüm, sanatçı veya playlist linklerinden 3D baskıya hazır anahtarlık modeli oluşturan masaüstü uygulaması.

[Özellikler](#özellikler) • [Demo](#demo) • [Kullanım](#kullanım) • [Krediler](#krediler) • [Lisans](#lisans)

![](https://github.com/ricdigi/spotify_keychain_3D_model/blob/master/Images/render_b.png?raw=true)

---

## ✨ Özellikler

- 🖥️ **Kullanıcı dostu arayüz** - Komut satırı gerektirmez
- 📁 **Birden fazla model desteği** - Farklı anahtarlık tasarımları arasından seçim
- 🔗 **Otomatik Spotify kod oluşturma** - Sadece link yapıştır
- 📦 **STL çıktısı** - 3D baskıya hazır format

---

## 🎬 Demo

![Uygulama Ekran Görüntüsü](screenshot.png)

1. Uygulamayı başlat
2. Spotify linkini yapıştır
3. Base model seç
4. "Generate" butonuna tıkla
5. STL dosyasını al ve 3D baskı yap!

---

## 📖 Kullanım

### Gereksinimler
- Python 3.8+
- cadquery
- requests  
- pillow

### Kurulum

```bash
pip install cadquery requests pillow
```

### Çalıştırma

```bash
python gui.py
```

### Base Modeller

`.step` dosyalarınızı `base_models` klasörüne yerleştirin. Uygulama otomatik olarak algılayıp listeler.

---

## 🙏 Krediler

Bu proje [Riccardo Di Girolamo](https://github.com/rickycraft) tarafından geliştirilen [spotify_keychain_3D_model](https://github.com/rickycraft/spotify_keychain_3D_model) projesinin fork'udur.

**Orijinal çalışma:**
- Spotify kod parse etme mantığı
- 3D model oluşturma algoritması
- Base anahtarlık STEP modelleri

**Bu fork'ta eklenenler:**
- Masaüstü GUI uygulaması (Tkinter)
- Çoklu base model seçimi
- Windows executable desteği

---

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

Original Copyright (c) 2024 Riccardo Di Girolamo

---

<p align="center">
  <a href="https://github.com/ottamina">Osman Teksoy</a><br>
  ⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!<br>
  Made with ❤️ in Turkey
</p>
