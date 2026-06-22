# PTSC Kripto - Gelişmiş Şifreleme Modülü

PTSC Kripto, `CustomTkinter` kullanılarak Python ile geliştirilmiş profesyonel bir şifreleme ve deşifreleme (kriptografi) uygulamasıdır. İçerisindeki algoritmalar sayesinde zamana bağlı dinamik tohum (seed) üretimi yapar ve mesajların bütünlüğünü kontrol eder.

## 🚀 Özellikler

- **Dinamik Tohum (Seed) Üretimi:** Saat bazlı (timestamp) dinamik tohum üretimi ile şifreleme algoritmasını güçlendirir.
- **Kimlik ve Bütünlük Doğrulama (Custom Hash):** Kendi içerisinde barındırdığı hash algoritması sayesinde mesajın yolda değiştirilip değiştirilmediğini veya bozulup bozulmadığını kontrol eder.
- **Simülasyon Terminali:** Yapılan tüm işlemlerin detayını (hash hesaplamaları, zaman damgaları, doğrulama adımları) eş zamanlı olarak gösteren canlı bir arayüz terminaline sahiptir.
- **Modern Arayüz:** CustomTkinter ile hazırlanmış karanlık (dark) temalı, kullanımı kolay bir yapıya sahiptir.

## 🛠️ Kurulum

Bu projeyi kendi bilgisayarınızda çalıştırmak için **Python 3.x**'in kurulu olması gerekmektedir. 

1. Projeyi bilgisayarınıza indirin (veya klonlayın).
2. Proje dizininde bir terminal (komut satırı) açın.
3. Gerekli kütüphaneleri yüklemek için aşağıdaki komutu çalıştırın:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Kullanım

Uygulamayı başlatmak için ana klasördeyken terminale aşağıdaki komutu yazın:
```bash
python main.py
```

### 🔒 Şifreleme (Encrypt)
1. Sol panelden **Şifrele** sekmesine geçin.
2. Gizlemek istediğiniz metni yazın ve **ŞİFRELE** butonuna basın.
3. Uygulama, metni şifreler, özel bir hash oluşturur ve saat bilgisini de ekleyerek `ŞifreliMetin|Hash|Saat` formatında bir paket çıkarır.
4. Çıkan şifreli veri, kullanım kolaylığı açısından Deşifrele sekmesine otomatik olarak kopyalanır.

### 🔓 Deşifreleme (Decrypt)
1. Sol panelden **Deşifrele** sekmesine geçin.
2. Size gönderilen veya önceden şifrelediğiniz `Metin|Hash|Saat` formatındaki paketi yapıştırın.
3. **DEŞİFRELE** butonuna basın.
4. Sistem, saati ve şifreli metni kullanarak orijinal metni kurtarmaya çalışır. Ardından orijinal hash ile yeni hesaplanan hash'i karşılaştırır:
   - Eğer her şey doğruysa: **[ ✔ GÜVENLİ / ONAYLANDI ]** uyarısı verilir ve şifreli mesaj gösterilir.
   - Eğer veri paketindeki tek bir harf bile değiştirilmişse (örneğin araya girilmişse) veya saat bozulmuşsa: **[ ❌ İHLAL TESPİT EDİLDİ / REDDEDİLDİ ]** uyarısı verilir. İstiyorsanız paketteki herhangi bir harfi değiştirerek bu güvenlik önlemini test edebilirsiniz.

## 📄 Lisans
Bu projenin tüm hakları saklıdır (All Rights Reserved). Kaynak kodlarının izinsiz kopyalanması, dağıtılması, değiştirilmesi veya ticari/bireysel amaçlarla kullanılması kesinlikle yasaktır. Proje sadece görüntüleme ve inceleme amaçlı olarak paylaşılmıştır.
