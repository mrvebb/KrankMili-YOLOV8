#  model_inference Açıklaması

Bu klasör, eğitilmiş YOLOv8 modelini kullanarak krank mili nesnesini gerçek zamanlı olarak kamera görüntüsü üzerinden algılayan kodu içerir. YOLOv8 modeli, belirli bir süre boyunca krank milinin görüntüde kalmasını izleyerek "var" olup olmadığını sayar.

---
### Kullanılan Kütüphaneler

- `cv2` → Kamera erişimi, görüntü işleme, metin ekleme
- `ultralytics.YOLO` → Eğitilmiş YOLOv8 modelini yükleyip tahmin alma
- `time` → Süre takibi (başlangıç ve sıfırlama)

---

###  Amaç
- Eğitilmiş `best.pt` modelini yükler.
- Bilgisayar kamerasını kullanarak canlı görüntü üzerinde krank mili nesnesini arar.
- Krank mili yeterli süre boyunca görünüyorsa bir adet olarak sayar.
- Görüntü üzerine sayaç, durum bilgisi ve uyarılar gibi metinleri ekleyerek kullanıcıya anlık geri bildirim sunar.

---

##  Ana Bileşenler

### MODEL_PATH
- Daha önce eğitilmiş modelin tam yoludur.Buraya eklenmelidir. (örneğin: `C:/Users/....../best.pt`).

###  Kamera Açma
- Varsayılan kamera (`cv2.VideoCapture(0)`) başlatılır.
- Kamera açılmazsa uygulama otomatik kapanır.

---

##  Sayım Mantığı
-İlk algıladıktan sonra nesne 10 saniye boyunca sürekli görünürse adet 1 olarak sayılır.40 saniye boyunca hiç görünmezse sayaç ve zamanlayıcı sıfırlanır ama 40 saniye içerisinde nesne tekrar görünürse toplam sayıya eklenmez.

- Bu sayede her krank mili sadece bir kez sayılmış olur.
- Sistem gereksiz tekrarlamayı önler.

---

##  Ekran Üzerindeki Bilgiler

Algılama sonucu ekranda canlı olarak gösterilir:

- Krank mili tespit edildi, sayım için bekleniyor...
- Krank mili sayıldı! TOPLAM:
- Krank mili görünümden çıktı. Yeni nesne için hazır.

Tüm bilgiler `cv2.putText()` fonksiyonu ile görüntüye eklenir.

---

##  Dikkat Edilmesi Gerekenler

- `MODEL_PATH` değişkenini bilgisayarındaki doğru `best.pt` dosyasına göre ayarlanmalı.
- Kamera düzgün çalışmıyorsa boş kare verir.
- Algılama performansı, görüntü kalitesi ve ışık koşullarına göre değişebilir.
- `CONF_THRESHOLD`(güven skoru) değerini artırarak yanlış pozitifleri azaltılabilir.
- Sadece 1 sınıf (krank mili) için eğitildiği için `if box.cls[0] == 0`
---
